
from operator import indexOf
import mysql.connector
from numpy import delete
from utils import *



class db ():
    
    def __init__(self, host ="localhost", user="root", password="", database="") :

        self.host = host
        self.user = user
        self.password = password
        self.database =database
        self.mode= 'dep'
        global conn
        try:
            conn = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database
                
            )
        except:
            log("could not connect to db")
        else:
            log("db connected succesfully")
            

        
    def run(self, query, data=[]):
        try:
            cursor =  conn.cursor(dictionary = True, buffered = True)  
            if(len(data) >0):
                if( type(data) is tuple):
                    data = [data]
                out = cursor.executemany(query, data)
            else:   
                out= cursor.execute(query)
            
        except mysql.connector.Error as e:
            log("could not run")
            log(e)
            return None,None,False     
        else:
            return out, cursor,True
            
    def verify(self, var, msg):
        if(var[2]) :
            log(msg)
    def createDb(self, name):
        self.verify(self.run("CREATE DATABASE "+name), 'DATABASE CREATED')
        
    
    def selectDb(self, name):
        q = self.run("USE "+name)
        if(q[2]):
            log('DATABASE SELECTED')
            self.database = name
        

#  ying       
    def c(self, ell):
    #initializatoin
        try:ell['id']  = ell['id'] 
        except:ell['id'] = None
        try:ell['fk']  = ell['fk'] 
        except:ell['fk'] = None
        try:ell['pk']  = ell['pk'] 
        except:ell['pk'] = None
    #decleration  
        row = ell['rows']
        name = ell['name']
        pk = ell['pk']
        id = ell['id']
        fk = ell['fk']     
        
        error_count = 0  
    #existance check        
        chk =self.chk(name)
        if(chk):
            log("table already exists")
        elif(not chk):   
        # varaible mapping    
            if(type(row) is list ):
                def ass(x):
                    if(x != id): 
                        return qoute(x)+' '+VAR
                    else:
                        return qoute(x)      
                q_row = list(map(ass, row))
            else:
                q_row = row 
        #id initilization
            if(id != None and id in row):
                if(type(q_row) is list): 
                    i =indexOf(q_row, qoute(id))
                    q_row[i] += ' INT AUTO_INCREMENT UNIQUE NOT NULL'
                    if(pk is None):
                        q_row[i] += ' PRIMARY KEY'
                elif(type(q_row) is dict):
                    q_row[id] += ' AUTO_INCREMENT UNIQUE NOT NULL'
                    if(pk is None):
                        q_row[id] += ' PRIMARY KEY'
            else:
    
                log('invalid id parameter')
                error_count += 1
        #computing row querys
            if(type(row) is dict):
                q_rows = stringify(q_row,',\n','(\n', key =qoute) 
            else:
                q_rows = stringify(q_row,',\n','(\n') 

        #priamry key
            if(pk != None  ):
                if(pk in row):
                    q_pk = ",\n PRIMARY KEY("+qoute(pk)+")"
                else:
                    log('invalid primary key parameter')
                    error_count +=1
            else:
                q_pk = ""    
        #foreign key
            if(fk != None ):
                if(fk[0] in row and (fk[0] == pk or fk[0] == id) ):
                    q_fk = ",\nFOREIGN KEY ("+qoute(fk[0])+") \n\tREFERENCES "+qoute(fk[1])+"("+qoute(fk[2])+")"+"\n\tON DELETE CASCADE\n"
                else:
                    log(fk[0]+' is not prirmary key')
                    error_count +=1
            else:
                q_fk = ""
        #final query
            if(error_count <1):
                query = "CREATE TABLE "+qoute(name)+" "+q_rows+q_pk+q_fk+");"
                log(query)
                out = self.run(query)
                if(out[2] ==1):
                    log("table created succesfully")
            else:
                log(str(error_count)+' error found')
                
        
#  insert       
    def insert (self, name, cols, data):
        if(type(data) is str and type(cols) is str):
            q_cols = par(qoute(cols))
            val = par(qoute(data,1))
        elif(type(cols) is tuple and type(data) is tuple):
            q_cols = stringify(cols,',','(', ')')  
            def func(s):
                return '\''+str(s)+'\''
            val = stringify(list(map(func, data)),',','(', ')')  
        else:
            q_cols = stringify(cols,',', '(', ')')  
            q_data =data
            val = stringify(s_x('%s',len(cols)), ',','(', ')')
        
        sql  = "INSERT INTO `"+name+"` "+q_cols+" VALUES "+val+";"        
        # log(sql)
        if(type(data) != list):
            res =self.run(sql)
        else:
            # log(q_data)
            res= self.run(sql, q_data)
        if(res[2]):
            conn.commit()
            log("insert success")
                    
        
    def fetch(self,table_name=None, item ='*', where='1', order = False, asc=True, dsc=False):
        error_count = 0
        q_from  =qoute(table_name)
        if(self.chk(table_name) <1):
            log('table does not exist')
        else:
     #fields
            if(item != '*'):
                q_item = ''
                if(item in self.get_fields(table_name)):
                    if(type(item) is str):
                        q_item = qoute(item)               
                    else:
                        q_item = stringify(list(map(qoute, item)), ',')
                else:
                    log('invalid column provided')
                    error_count += 1
            else:
                q_item = '*'
        #WHERE  
            if(where != '1'):
                where= stringify(self.where_pros(where, table_name))
            q_where = 'WHERE '+where
        # ORDER
            if(order):
                if(order in self.get_fields(table_name)):
                    if(dsc):
                        sort = 'DESC'
                    else:
                        sort = 'ASC'
                    q_order = stringify(["ORDER BY",qoute(order),sort])
                else:
                    log('invalid order field provided')
                    error_count += 1
                    q_order = ''
            else:
                q_order = ''     
        # FINAL CHECK
            query = stringify(["SELECT",q_item," FROM ",q_from,q_where,q_order])
            if(error_count <1):
                res = self.run(query)[1].fetchall()
                return res
            else:
                log('refused to run \n'+str(error_count)+' error found,\nplease chack your code again')
                return False
    # update        
    def update(self,ell):
    #initializatoin
        try:ell['table']  = ell['table'] 
        except:ell['table'] = False
        try:ell['fields']  = ell['fields'] 
        except:ell['fields'] = False
        try:ell['where']  = ell['where'] 
        except:ell['where'] = False    
    #decleration  
        tbl_name = ell['table']  
        fields =  ell['fields']
        where = ell['where']
        error_count =0
    
        if(tbl_name and self.chk(tbl_name)):
            q_tbl_name  = qoute(tbl_name)
            if(fields):
                q_fields = stringify(fields, ',', key=qoute,value=qoute2 ,mid = ' = ')
            else:
                log('no update firld provided')
                error_count += 1
            if(where):
                q_where  = stringify(self.where_pros(where, tbl_name))
            else:
                q_where = 1
        else:
            log('invalid table name')
            error_count += 1
            
        if(error_count <1):
            query = stringify(['UPDATE ', q_tbl_name,'SET',q_fields,'WHERE',q_where])
            out = self.run(query)
            if(out[2]):
                conn.commit()
                log('UPDATE SUCCESSFUL')
# yang   
    def delete(self, tbl, where):
        if(self.chk(tbl)):
            q_where =  stringify(self.where_pros(where, tbl))
            q_tbl = qoute(tbl)
            out = self.run(stringify(["DELETE FROM",q_tbl, 'WHERE', q_where])) 
            if(out[2]):
                log('TABLE DELETED')
                conn.commit()
                
        else:
            log('table does not exist')
    def empty(self,tbl):
        self.verify(self.run("TRUNCATE "+qoute(tbl)), 'TABLE EMPTIED') 
    def drop(self, tbl):
        if(type(tbl) is str):
            self.verify(self.run("DROP TABLE "+qoute(tbl)), 'TABLE DELETED')
        else:
            self.verify(self.run("DROP TABLE "+stringify(tbl, ',',value=qoute)), 'TABLE DELETED')
            
    def kill_la_kill(self, db):
         self.verify(self.run("DROP DATABASE "+qoute(db)), 'DATABASE DELETED')
    
    
    # logics --------------------------------------------
    def chk(self, tbl):
        tbls =sub_arr(self.run('SHOW TABLES')[1].fetchall(), 'Tables_in_'+self.database)
        out = False
        if(tbl in tbls):
            out = True
        return out    
    def get_columns(self, table_name):
        return self.run('DESCRIBE '+self.database+'.'+table_name)[1].fetchall()
    def get_fields(self, table_name):
        return sub_arr(self.run('DESCRIBE '+self.database+'.'+table_name)[1].fetchall(), 'Field')
    def where_pros(self, where, fro):
        x = 0
        operand = ['OR', '||','AND',  '&' ,'=', 'LIKE', '!', 'NOT', '!=', 'BETWEEN', 'IS', 'NULL', '<', '>','<=','>=' ]
        w_arr = where.split()
        atr_arr = self.get_fields(fro)
        for x in w_arr:
            if(x in atr_arr and x not in operand):
                w_arr[indexOf(w_arr, x)] = qoute(x,0)
            elif(x not in atr_arr and x.upper() not in operand and is_int(x) and x[0] != '"' and x[0] != "'"):
                w_arr[indexOf(w_arr, x)] = qoute(x, 1)
        return w_arr
        