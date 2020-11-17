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
col_name += str(period)
col = db[col_name]
name_list = [x for x in col.find({})]
print('done')
name_list.sort()
b_saham_ = {}
f_saham_ = {}
all_data_ = []
for name in name_list:
    print(name)
    b_saham_[name] = []
    f_saham_[name] = []
    data_saham = [x for x in col.find({'name': name})]
    data_saham.sort(key= lambda y: y['data']['time'])
    for data_ in data_saham:
        _data = data_['data']
        low_ = _data['low']
        high_ = _data['high']
        close_ = _data['close']
        data__ = {}
        data__['name'] = data_['name']
        data__['time'] = datetime.fromtimestamp(_data['time']/1000)
        data__['buy_price'] = low_ if ((high_ - low_) / high_) * 100 < 20 else close_
        data__['sell_price'] = high_ if ((high_ - low_) / high_) * 100 < 20 else close_
        _ema_stat = _data['ema_stat']
        _sma_stat = _data['sma_stat']
        _buy_stat = 0
        _sell_stat = 0
        _ma_stat_sell = (_ema_stat.count(1) + _sma_stat.count(1)) / 5
        _ma_stat_buy = (_ema_stat.count(2) + _sma_stat.count(2)) / 5
        _buy_stat += _ma_stat_buy
        _sell_stat += _ma_stat_sell
        _buy_stat += 1 if _data['sto_stat'] == 2 else 0
        _sell_stat += 1 if _data['sto_stat'] == 1 else 0
        data__['bayok_stat'], data__['firza_stat'] = 0, 0
        # if _buy_stat > _sell_stat:
        data__['bayok_stat'] = 2 if _buy_stat > _sell_stat and _buy_stat >= 3 else 1 if _buy_stat < _sell_stat and _sell_stat >= 3 else 0
        if _data['bol_stat'] == _data['ses_stat']:
            data__['firza_stat'] = _data['bol_stat']
        if data__['bayok_stat'] or data__['firza_stat']:
            if data__['bayok_stat'] == 2:
                if len(b_saham_[name]) > 0:
                    if b_saham_[name][-1]['bayok_stat'] == 1:
                        b_saham_[name].append(data__)
                    # else:
                    #     print('saham sudah ada')
                else:
                    b_saham_[name].append(data__)
            elif data__['bayok_stat'] == 1:
                if len(b_saham_[name]) > 0:
                    if b_saham_[name][-1]['bayok_stat'] == 2:
                        b_saham_[name].append(data__)
                #     else:
                #         print('saham belum ada')
                # else:
                #     print('saham belum ada')

for key in b_saham_:
    print(key, b_saham_[key])