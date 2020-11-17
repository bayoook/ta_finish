from pymongo import MongoClient
from pprint import pprint
client = MongoClient()
db = client['dataSaham']
pipeline = [
    {"$match": {"date":"02122019", "period":1, "name":"BBCA"}},
    {"$sort": { "_id": 1}},
    {"$group": {
        "_id": "$name",
        "data": {"$addToSet": "$data"},
    }}
]

a = list(db.data.aggregate(pipeline))
d = {x['_id'] : x['data'] for x in a}
print(d)
# for x in a:
    