# pydb
a database management system library that operates based on mysql db

##usage:
from utils import *
import db

#for initialzing a database connection
dabase =db.db(host, user, password, database)

host= the host name of your database
user = username
password= password
database is optional for now you can add a databse later with :=
dabase.selectDb('mrpepe')

#Creating database := # dabase.createDb("new_test")

## creating table :=
dabase.c({
  'name':'another5',
   'rows':['names', 'keys'],
   'pk': 'names'
   'id':'keys',
   'fk':('keys','another2', 'keys')
})
or
dabase.c({
  'name':'another5',
   'rows':{'names':VAR, 'keys':INT},
   'id':'keys',
   'fk':('keys','another2', 'keys')
})

note:
'fk' (foreign key) and 'id'(makig a row an id row) and 'pk' (primary key) are all optional 


## insert
dabase.insert('table_name', ('name', 'password', 'user_id', 'access_level'),('iorsase', '12345','6','user

##select or fetch
  dabase.fetch('table_name','row or (rows)',where='access_level = admin', order='user_id')
 for order you can either set asc = True or desc =True
 
## update
  dabase.update({
      'table':'users',
      'fields':{
          'name':'jerimyS',
      },
      'where':'password = asdfg'
  })
## delte 
 dabase.delete('table_name', 'access_level = amin')
 
##empty
 dabase.empty('table_name')
 
##drop 
 dabase.drop(('another3', 'another5', 'another2'))












