import json
from itertools import groupby
from pymongo import MongoClient
from datetime import date, datetime
from statistics import stdev
import linecache
import sys
client = MongoClient()
db = client['dataSaham']

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

waktu = 1
datee = f"{date.today().strftime('%d%m%Y')}"
# datee = '20122019'
print(datee)
# db.data.remove({'date': datee, 'period': waktu})
# print('get data 5 days before')
# a = [x for x in db.data.find({"period":1}).distinct('date')]
# a = sorted(a, key=lambda x: datetime.strptime(x, '%d%m%Y'))
# a = a[-5:]
# print(a)
# # a = ['06112019', '08112019', '11112019', '12112019', '13112019', '14112019', '15112019', '18112019', '20112019', '21112019', '22112019', '25112019', '26112019', '27112019', '28112019', '29112019', '02122019', '03122019', '05122019']
# # print(a)
# # exit(1)
# name = ''
# data_all = {}
# ddd = []
# cursor_ = db.data.find({"$or":[{'date':x, 'period': waktu} for x in a]}).sort('_id', 1)
# # for x in a:
# #     cursor_ = db.data.find({'date':x, 'period': waktu})
# for key in cursor_:
#     try:
#         if key['name'] not in data_all:
#             data_all[key['name']] = []
#         if len(data_all[key['name']]) >= 101:
#             data_all[key['name']].pop(0)
#         data_all[key['name']].append(key['data'])
#     except Exception as e:
#         print(e)
#         pass
# print('processing date today')
f = open('dbs_' + datee + '.txt', 'r')
print('dbs_' + datee + '.txt')
ddata = f.read().splitlines()
ddata = [json.loads(x.replace("'",'"')) for x in ddata]
ddata.sort(key=lambda y: y['sec'])
for k, v in groupby(ddata, key=lambda y: y['sec']):
    lv = list(v)
    vol_arr = [int(x['vol'].replace(',','')) for x in lv]
    print(k, sum(vol_arr))
    lv.sort(key=lambda y: y['price'])
    for k1, v1 in groupby(lv, key=lambda y: y['price']):
        lv1 = list(v1)
        vol_arr = [int(x['vol'].replace(',','')) for x in lv1]
        print(k1, sum(vol_arr))
    