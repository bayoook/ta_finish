from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.dataSaham
cursor_ = db.data.find({'date':'02012020'})
print(cursor_.count())