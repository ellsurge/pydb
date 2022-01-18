from utils import *
import db

dabase =db.db()
dabase.selectDb('mrpepe')

# dabase.createDb("new_test")

# dabase.c({
#     'name':'another5',
#     'rows':['names', 'keys'],
#     'id':'keys',
#     'fk':('keys','another2', 'keys')
# })

# dabase.drop(('another3', 'another5', 'another2'))

# dabase.update({
#     'table':'users',
#     'fields':{
#         'name':'jerimyS',

#     },
#     'where':'password = asdfg'
# })

# dabase.delete('users', 'access_level = amin')

# dabase.insert('users', ('name', 'password', 'user_id', 'access_level'),('iorsase', '12345','6','user'))

# dabase.drop()

# dabase.empty('meal')

# print(dabase.fetch('users', 'name'))

# dabase.fetch('users',where='access_level = admin', order='user_id', dsc = True)
#     'where':
# })

# dabase.fetch({})

# dabase.kill_la_kill('test')