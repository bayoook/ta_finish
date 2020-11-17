import json
from pymongo import MongoClient
from datetime import datetime
from itertools import groupby
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import os.path
from os import path
import sys

client = MongoClient('mongodb://localhost:27017/')
db = client.dataSaham
period = int(sys.argv[1])
col_name = 'data'
if period != 1:
    col_name += str(period)
date_list = [x for x in db[col_name].distinct('date')]
date_list = sorted(date_list, key=lambda x: datetime.strptime(x, '%d%m%Y'))
date_list = date_list[:-2]
print(date_list)
# kontol
#open('hasil_.csv', 'w').write('')
hasil_bayok = 0
hasil_firza = 0
all_data_ = []
hoh = 0
os.system('rm data/hasil/' + str(period) + '/hasil_bayok.csv')
os.system('rm data/hasil/' + str(period) + '/hasil_firza.csv')
for date_ in date_list:
    print('process', date_)
    data_list = db[col_name].find({'date': date_, 'period': period})
    for data_ in data_list:
        _data = data_['data']
        low_ = _data['low']
        high_ = _data['high']
        close_ = _data['close']
        data__ = {}
        data__['name'] = data_['name']
        data__['time'] = datetime.fromtimestamp(_data['time']/1000)
        data__['buy_price'] = low_ if (
            (high_ - low_) / high_) * 100 < 20 else close_
        data__['sell_price'] = high_ if (
            (high_ - low_) / high_) * 100 < 20 else close_
        _ma_stat = _data['ema_stat']
        _data['ma_stat'] = 1 if _ma_stat.count(1) > 2 else 2
        data__['bayok_stat'], data__['firza_stat'] = 0, 0
        # data__['sum_stat'] = 0 
        if _data['ma_stat'] == _data['sto_stat']:
            data__['bayok_stat'] = _data['ma_stat']
        if _data['bol_stat'] == _data['ses_stat']:
            data__['firza_stat'] = _data['bol_stat']
        if data__['bayok_stat'] or data__['firza_stat']:
            all_data_.append(data__)
    print('done', date_)
all_data_.sort(key=lambda y: y['name'])
print(len(all_data_))
al = []
for k, v in groupby(all_data_, key=lambda y: y['name']):
    v_ = list(v)
    sum_ = 0
    for i, k_ in enumerate(v_):
        # try:
        #     lah = json_normalize(d)
        # except:
        #     continue

        if k_['bayok_stat'] == 2 and v_[i-1]['bayok_stat'] == 1:
            d = {
                'name': [k],
                'buy_price': [v_[i-1]['buy_price']],
                'buy_time': [v_[i-1]['time']],
                'sell_price': [k_['sell_price']],
                'sell_time': [k_['time']],
                'lot': [1],
                'profit': [(k_['sell_price'] - v_[i-1]['buy_price']) * 100]
            }
            hasil_bayok += (k_['sell_price'] - v_[i-1]['buy_price']) * 100
            neme = 'data/hasil/'+ str(period) +'/hasil_bayok.csv'
            # try:
            #     lah = json_normalize(k_)
            # except:
            #     continue
            lah = pd.DataFrame.from_dict(d)
            if path.isfile(neme) == False:
                hed = True
            elif path.isfile(neme) == True:
                hed = False
            lah.to_csv(neme, mode='a', index=False, header=hed)
        if k_['firza_stat'] == 2 and v_[i-1]['firza_stat'] == 1:
            d = {
                'name': [k],
                'buy_price': [v_[i-1]['buy_price']],
                'buy_time': [v_[i-1]['time']],
                'sell_price': [k_['sell_price']],
                'sell_time': [k_['time']],
                'lot': [1],
                'profit': [(k_['sell_price'] - v_[i-1]['buy_price']) * 100]
            }
            hasil_firza += (k_['sell_price'] - v_[i-1]['buy_price']) * 100
            neme = 'data/hasil/'+ str(period) +'/hasil_firza.csv'
            # try:
            #     lah = json_normalize(k_)
            # except:
            #     continue
            lah = pd.DataFrame.from_dict(d)
            if path.isfile(neme) == False:
                hed = True
            elif path.isfile(neme) == True:
                hed = False
            lah.to_csv(neme, mode='a', index=False, header=hed)
print(hasil_bayok, hasil_firza)
sol = {'name': ['Total'], 'buy_price': [hasil_bayok]}
sol = pd.DataFrame.from_dict(sol)
sol.to_csv('data/hasil/'+ str(period) +'/hasil_bayok.csv', mode='a', index=False, header=False)

sol2 = {'name': ['Total'], 'buy_price': [hasil_firza]}
sol2 = pd.DataFrame.from_dict(sol2)
sol2.to_csv('data/hasil/'+ str(period) +'/hasil_firza.csv', mode='a', index=False, header=False)
print("Done All")

# exit(1)
