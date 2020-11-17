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
# datee = '26122019'
print(datee)
db.data_chart.remove({'date': datee, 'period': waktu})
print('get data 5 days before')
a = [x for x in db.data_chart.find({"period": 1}).distinct('date')]
a = sorted(a, key=lambda x: datetime.strptime(x, '%d%m%Y'))
a = a[-5:]
print(a)
name = ''
data_all = {}
ddd = []
cursor_ = db.data_chart.find({"$or": [{'date': x, 'period': waktu} for x in a]}).sort('_id', 1)
for key in cursor_:
    try:
        if key['name'] not in data_all:
            data_all[key['name']] = []
        if len(data_all[key['name']]) >= 101:
            data_all[key['name']].pop(0)
        data_all[key['name']].append(key['data'])
    except Exception as e:
        print(e)
        pass
print('processing date today')
f = open('data_minute_' + datee + '.txt', 'r')
print('data_minute_' + datee + '.txt')
ddata = f.read().splitlines()
# print(len(ddata))
# exit(1)
ddata = [json.loads(x.replace("'", '"')) for x in ddata]
ddata.sort(key=lambda y: y['saham'])
data_s = []
fast_per = []
smooth_per = []
ope = []
eman = 0
ses = 0
statusk = 0
for k, v in groupby(ddata, key=lambda y: y['saham']):
    arr_ = []
    for data in list(v):
        if int(data['vol']) == 0:
            continue
        try:
            try:
                data['high'] = int(data['high'])
                data['low'] = int(data['low'])
                data['open'] = int(data['open'])
                data['close'] = int(data['close'])
                data['vol'] = int(data['vol'])
                data['sum'] = ((data['high'] + data['low'] + data['close']) / 3) * data['vol']
                data['avg'] = data['sum'] / data['vol']
                data['smooth_atas'] = False
                try:
                    data_all[k].append(data)  # memasukkan data persaham permenit, ke dalam data_all
                except:  # jikalau tidak ada data sebelumnya sama sekali
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
                        smoothed = sum([x['fast_x'] for x in data_all[k][-3:]]) / len(
                            [x['fast_x'] for x in data_all[k][-3:]])
                    except:
                        data['fast'] = fast_line
                        smoothed = sum([x['fast'] for x in data_all[k][-3:]]) / len(
                            [x['fast'] for x in data_all[k][-3:]])

                    data['fast'] = smoothed  # Stochastic Fast Line
                    smoothed = sum([x['fast'] for x in data_all[k][-3:]]) / len([x['fast'] for x in data_all[k][-3:]])
                    data['smooth'] = smoothed  # Stochastic  Smooth Line
                    # End Stochastic

                    # EMA
                    try:
                        # Get value EMA Before
                        eman = [x for x in data_all[k][-2]['ema']]
                    except:
                        eman = [0, 0, 0, 0, 0]

                    # Ema<n> | n = jumlah data
                    ema5 = ((data['close'] - eman[0]) * (2 / (len(data_all[k][-5:]) + 1))) + (eman[0])
                    ema10 = ((data['close'] - eman[1]) * (2 / (len(data_all[k][-10:]) + 1))) + (eman[1])
                    ema20 = ((data['close'] - eman[2]) * (2 / (len(data_all[k][-20:]) + 1))) + (eman[2])
                    ema50 = ((data['close'] - eman[3]) * (2 / (len(data_all[k][-50:]) + 1))) + (eman[3])
                    ema100 = ((data['close'] - eman[4]) * (2 / (len(data_all[k][-100:]) + 1))) + (eman[4])
                    data['ema'] = [ema5, ema10, ema20, ema50, ema100]
                    # End Ema

                    # SES single exponential smoothing
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
                    up = data['sma'][2] + (m * std)  # Upper Band
                    lo = data['sma'][2] - (m * std)  # Lower Band
                    data['bol_hi'] = up
                    data['bol_lo'] = lo
                    # Middle Band using SMA
                    # End Bollinger Band

                    # Predict Process | 1 = jual, 2 = beli, 0 = gaada sinyal

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

                    # SMA
                    data['sma_stat'] = [1 if x >= data['close'] else 2 for x in data['sma']]

                    # Stochastic

                    if data['smooth'] > data['fast']:
                        data['smooth_atas'] = True
                    try:
                        if data['smooth_atas'] and not data_all[k][-2]['smooth_atas'] or data_all[k][-2][
                            'smooth_atas'] and not data['smooth_atas']:
                            if data['smooth'] >= 80:
                                data['sto_stat'] = 1
                            elif data['smooth'] <= 20:
                                data['sto_stat'] = 2
                            else:
                                data['sto_stat'] = 0
                        else:
                            data['sto_stat'] = 0
                    except:
                        data['sto_stat'] = 0
                    # end stochastic

                    if data['bol_stat'] == 1:
                        sell_signal += 1
                    elif data['bol_stat'] == 2:
                        buy_signal += 1

                    if data['ses_stat'] == 1:
                        sell_signal += 1
                    elif data['ses_stat'] == 2:
                        buy_signal += 1
                    if data['ema_stat'].count(1) >= 4:  # [1, 1, 1, 1, 2]
                        sell_signal += 1
                    elif data['ema_stat'].count(2) >= 4:
                        buy_signal += 1

                    if data['sto_stat'] == 1:
                        sell_signal += 1
                    elif data['sto_stat'] == 2:
                        buy_signal += 1

                    # Write Predict to file
                    # kode_saham status(1=jual, 2=beli) timestamp(ms) vote(sell) volte(buy) open high low close
                    try:
                        ro = open('data/order/order_' + datee + '.txt', 'r')
                        so = ro.read().splitlines()
                        ro.close()
                    except Exception as e:
                        so = ['']
                    ro = open('data/order/order_' + datee + '.txt', 'a')
                    if sell_signal >= 3:
                        data['status'] = '1'  # jual
                        value_save = k + ' ' + str(data['status']) + ' ' + str(data['time']) + ' ' + str(
                            sell_signal) + ' ' + str(buy_signal) + ' ' + str(data['open']) + ' ' + str(
                            data['high']) + ' ' + str(data['low']) + ' ' + str(data['close'])
                        if value_save not in so:
                            ro.write(value_save + '\n')
                    elif buy_signal >= 3:
                        data['status'] = '2'  # beli
                        value_save = k + ' ' + str(data['status']) + ' ' + str(data['time']) + ' ' + str(
                            sell_signal) + ' ' + str(buy_signal) + ' ' + str(data['open']) + ' ' + str(
                            data['high']) + ' ' + str(data['low']) + ' ' + str(data['close'])
                        if value_save not in so:
                            ro.write(value_save + '\n')
                    else:
                        data['status'] = '0'
                    ro.close()
                    # End Predict

                # Move data to array
                del data_all[k][-1]
                data_all[k].append(data)
                if len(data_all[k]) > 101:
                    del data_all[k][0]

                # This array for mongo insert
                arr_.append({
                    "date": datee,
                    "name": k,
                    "period": waktu,
                    "data": data
                })

            except Exception as e:
                PrintException()
        except Exception as e:
            PrintException()
    # print(len(arr_))
    try:
        db.data_chart.insert_many(arr_)
        print('done insert', k, len(arr_), arr_[-1]['data']['time'])
    except:
        # print(len(arr_))
        # PrintException()
        continue
