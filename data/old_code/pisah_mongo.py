from pymongo import MongoClient
from datetime import datetime
client = MongoClient('mongodb://localhost:27017/')
db = client.dataSaham
datetime_list = db.data.find({'period': 1}).distinct('date')
a = sorted(datetime_list, key=lambda x: datetime.strptime(x, '%d%m%Y'))
print(a)
for x in datetime_list:
    data_list = [x for x in db.data.find({'date': x, 'period': 1})]
    print(len(data_list))
