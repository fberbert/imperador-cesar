import shelve

#  db = shelve.open('membros', writeback=True)
#  db['King_Salame']['nickname'] = 'King Salame'
#  db.close()

db = shelve.open('guerra', writeback=True)
db['message_id'] = 0
db.close()
