import json
from pymongo import MongoClient
from datetime import datetime, timedelta
from itertools import groupby
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import os.path
from os import path
import sys
from statistics import stdev

client = MongoClient('mongodb://localhost:27017/')
db = client.dataSaham
period_ = int(sys.argv[1])
col_name = 'data' + str(period_)
remove = db[col_name].remove({'period':period_})
print(remove)
date_total = period_ * 2
date_list = db.data.find({'period':1}).distinct('date')
date_list = sorted(date_list, key=lambda x: datetime.strptime(x, '%d%m%Y'))
def olah_data(datetime_today):
    len_process = 0
    print("processing", datetime_today)
    db[col_name].remove({'date': datetime_today, 'period': period_})
    # print('get data 5 days before')
    # print(db.data.find({"period":period_}).distinct('date'))
    a = [x for x in db[col_name].find({"period":period_}).distinct('date')]
    # print(a)
    a = sorted(a, key=lambda x: datetime.strptime(x, '%d%m%Y'))
    a = a[-date_total:]
    name = ''
    data_all = {}
    # statusk
    ddd = []
    print(a)
    # exit(1)
    if len(a) > 0: 
        cursor_ = [x for x in db[col_name].find({"$or":[{'date':x, 'period': period_} for x in a]})]
    else:
        cursor_ = []
    cursor_.sort(key=lambda x: datetime.strptime(x['date'], '%d%m%Y'))
    print('len data before', len(cursor_))
    # date__ = {x['date'] for x in cursor_}
    # print('date', date__)
    # print('processing date before')
    day = ''
    for key in cursor_:
        if day != key['date']:
            print(key['date'], end = ', ')
            day = key['date']
        try:
            if key['name'] not in data_all:
                data_all[key['name']] = []
            if len(data_all[key['name']]) >= 101:
                data_all[key['name']].pop(0)
            data_all[key['name']].append(key['data'])
        except Exception as e:
            print(e)
            pass
    print()
    # print('done')
    # print('processing date today')
    data_saham = db.data.find({'date': datetime_today, 'period': 1})
    data_saham = [x for x in data_saham]
    data_saham.sort(key=lambda y: y['name'])
    # print(data_saham[0])

    # {
    #     '_id': ('5df67cc4fef4c0a0eea1356f'), 
    #     'date': '12122019', 
    #     'name': 'AALI', 
    #     'period': 1, 
    #     'data': {
    #         'time': 1576116180000.0, 
    #         'high': 13300, 
    #         'low': 13300, 
    #         'open': 13300, 
    #         'close': 13300, 
    #         'vol': 200, 
    #         'sum': 2660000,
    #         'avg': 13300.0, 
    #         'fast_x': 0.0, 
    #         'fast': 0.0, 
    #         'smooth': 11.111111111111112, 
    #         'ema': [13329.765136626955, 13345.550166592016, 13350.266772808793, 13348.583456154576, 13355.085427141204], 
    #         'ses': 13345.509808928471, 
    #         'sma': [13335.0, 13361.666666666668, 13353.75, 13338.166666666664, 13357.749999999998], 
    #         'bol_hi': 13412.358374149671, 
    #         'bol_lo': 13295.141625850329, 
    #         'bol_stat': 0, 
    #         'ses_stat': 1, 
    #         'ema_stat': [1, 1, 1, 1, 1], 
    #         'sma_stat': [1, 1, 1, 1, 1], 
    #         'sto_stat': 2, 
    #         'status': '0'
    #     }
    # }

    def get_key(x):
        # group by 30 minutes
        d = datetime.fromtimestamp(x['data']['time'])
        k = d + timedelta(minutes=-(d.minute % period_)) 
        return datetime(k.year, k.month, k.day, k.hour, k.minute, 0)

    for k, x in enumerate(data_saham):
        data_saham[k]['data']['time'] /= 1000
    print('len data today', len(data_saham))
    arr_ = []
    for k, v in groupby(data_saham, key= lambda y: y['name']):
        lv = list(v)
        lv.sort(key=get_key)
        # print(k, end=' ')
        eman = 0
        ses = 0
        statusk = 0
        for k1, v1 in groupby(lv, key=get_key):
            v2 = list(v1)
            k1 += timedelta(minutes=period_)
            # print(k1, len(v2))
            try:
                data = {
                    'time': datetime.timestamp(k1) * 1000,
                    'high': max([x['data']['high'] for x in v2]),
                    'low': min([x['data']['low'] for x in v2]),
                    'open': v2[0]['data']['open'],
                    'close': v2[-1]['data']['close'],
                    'vol': sum([x['data']['vol'] for x in v2]),
                    'sum': sum([x['data']['sum'] for x in v2]),
                    'avg': sum([x['data']['sum'] for x in v2])/sum([x['data']['vol'] for x in v2]),
                }
                # print(data)
                try:
                    data_all[k].append(data)
                except:
                    data_all[k] = []
                    data_all[k].append(data)
                if data != {}:
                    av = float(data["avg"])
                    c = int(data["close"])

                    # Stochastic
                    low = min([x['low'] for x in data_all[k][-14:]])
                    high = max([x['high'] for x in data_all[k][-14:]])
                    if high - low == 0:
                        high += 0.000000001
                    fast_line = ((c - low) / (high - low)) * 100

                    try:
                        data['fast_x'] = fast_line
                        smoothed = sum([x['fast_x'] for x in data_all[k][-3:]]) / len([x['fast_x'] for x in data_all[k][-3:]])
                    except:
                        data['fast'] = fast_line
                        smoothed = sum([x['fast'] for x in data_all[k][-3:]]) / len([x['fast'] for x in data_all[k][-3:]])
                    
                    data['fast'] = smoothed # Stochastic Fast Line
                    smoothed = sum([x['fast'] for x in data_all[k][-3:]]) / len([x['fast'] for x in data_all[k][-3:]])
                    data['smooth'] = smoothed # Stochastic  Smooth Line
                    # End Stochastic

                    # EMA
                    try:
                        # Get value EMA Before
                        eman = [x for x in data_all[k][-2]['ema']]
                    except:
                        eman = [0, 0, 0, 0, 0]
                    
                    # Ema<n> | n = periode
                    ema5 = ((data['close'] - eman[0]) * (2 / (len(data_all[k][-5:]) + 1))) + (eman[0])
                    ema10 = ((data['close'] - eman[1]) * (2 / (len(data_all[k][-10:]) + 1))) + (eman[1])
                    ema20 = ((data['close'] - eman[2]) * (2 / (len(data_all[k][-20:]) + 1))) + (eman[2])
                    ema50 = ((data['close'] - eman[3]) * (2 / (len(data_all[k][-50:]) + 1))) + (eman[3])
                    ema100 = ((data['close'] - eman[4]) * (2 / (len(data_all[k][-100:]) + 1))) + (eman[4])
                    data['ema'] = [ema5, ema10, ema20, ema50, ema100]
                    # End Ema

                    # SES
                    try:
                        # Get value EMA 50 before
                        ses = data_all[k][-2]['ema'][3]
                    except:
                        ses = float(data["avg"])
                    ses_fin = ses + 0.1 * (c - ses)
                    ses = ses_fin
                    data['ses'] = ses_fin

                    # SMA
                    # sma<n> | n = periode
                    tp = [(x['high'] + x['low'] + x['close']) / 3 for x in data_all[k]]
                    sma5 = sum(tp[-5:]) / len(tp[-5:])
                    sma10 = sum(tp[-10:]) / len(tp[-10:])
                    sma20 = sum(tp[-20:]) / len(tp[-20:])
                    sma50 = sum(tp[-50:]) / len(tp[-50:])
                    sma100 = sum(tp[-100:]) / len(tp[-100:])
                    data['sma'] = [sma5, sma10, sma20, sma50, sma100]
                    # End SMA

                    # Bollinger Band
                    m = 2
                    try:
                        std = stdev(tp[-20:])
                    except:
                        std = 0
                    up = data['sma'][2] + (m * std) # Upper Band
                    lo = data['sma'][2] - (m * std) # Lower Band
                    data['bol_hi'] = up
                    data['bol_lo'] = lo
                    # Middle Band using SMA
                    # End Bollinger Band
                    
                    # Predict Process
                    # Bollinger Band
                    sell_signal = 0
                    buy_signal = 0
                    if float(data["high"]) > float(data["bol_hi"]) \
                            or float(data["open"]) > float(data["bol_hi"]) \
                            or float(data["close"]) > float(data["bol_hi"]) \
                            or float(data["low"]) > float(data["bol_hi"]):
                        data['bol_stat'] = 1
                    elif float(data["high"]) < float(data["bol_lo"]) \
                            or float(data["open"]) < float(data["bol_lo"]) \
                            or float(data["close"]) < float(data["bol_lo"]) \
                            or float(data["low"]) < float(data["bol_lo"]):
                        data['bol_stat'] = 2
                    else:
                        data['bol_stat'] = 0
                    
                    # SES
                    data['ses_stat'] = 1 if float(data["ses"]) >= float(data["close"]) else 2

                    # EMA
                    data['ema_stat'] = [1 if x >= data['close'] else 2 for x in data['ema']]
                    data['sma_stat'] = [1 if x >= data['close'] else 2 for x in data['sma']]

                    # Stochastic
                    if (statusk == 1 and data["smooth"] <= data['fast']) or (
                            statusk == 0 and data['fast'] <= data['smooth']):
                        statusk = 1 if data["smooth"] >= data['fast'] else 0
                        if float(data["smooth"]) > float(80):
                            data['sto_stat'] = 1
                        elif float(data["smooth"]) < float(20):
                            data['sto_stat'] = 2
                        else:
                            data['sto_stat'] = 0
                    else:
                        data['sto_stat'] = 0
                    
                    # if data['bol_stat'] == 1:
                    #     sell_signal += 1
                    # elif data['bol_stat'] == 2:
                    #     buy_signal += 1

                    # if data['ses_stat'] == 1:
                    #     sell_signal += 1
                    # elif data['ses_stat'] == 2:
                    #     buy_signal += 1

                    # if data['ema_stat'][2] == 1:
                    #     sell_signal += 1
                    # elif data['ema_stat'][2] == 2:
                    #     buy_signal += 1

                    # if data['sto_stat'] == 1:
                    #     sell_signal += 1
                    # elif data['sto_stat'] == 2:
                    #     buy_signal += 1
                    # # Write Predict to file
                    # try:
                    #     ro = open('data/order/order_' + datetime_today + fFoot, 'r')
                    #     so = ro.read().splitlines()
                    #     ro.close()
                    # except Exception as e:
                    #     so = ['']
                    # ro = open('data/order/order_' + datetime_today + fFoot, 'a')
                    # if sell_signal >= 3:
                    #     data['status'] = '1'
                    #     value_save = k + ' ' + str(data['status']) + ' ' + str(data['time']) + ' ' + str(sell_signal) + ' ' + str(buy_signal) + ' ' + str(data['open']) + ' ' + str(data['high'])+ ' ' + str(data['low']) + ' ' + str(data['close'])
                    #     if value_save not in so:
                    #         ro.write(value_save + '\n')
                    # elif buy_signal >= 3:
                    #     data['status'] = '2'
                    #     value_save = k + ' ' + str(data['status']) + ' ' + str(data['time']) + ' ' + str(sell_signal) + ' ' + str(buy_signal) + ' ' + str(data['open']) + ' ' + str(data['high'])+ ' ' + str(data['low']) + ' ' + str(data['close'])
                    #     if value_save not in so:
                    #         ro.write(value_save + '\n')
                    # else:
                    #     data['status'] = '0'
                    # ro.close()
                    # End Predict
                
                # Move data to array
                del data_all[k][-1]
                data_all[k].append(data)
                if len(data_all[k]) > 101:
                    del data_all[k][0]
                
                # This array for mongo insert
                arr_.append({
                    "date": datetime_today,
                    "name": k,
                    "period": period_,
                    "data": data
                })
            except Exception as e:
                print("Error", e, "at", k, k1)
    try:
        db[col_name].insert_many(arr_)
        len_process += len(arr_)
    except Exception as e:
        print(e)
    print('done', datetime_today, len_process)

for x in date_list:
    olah_data(x)
# exit(1)