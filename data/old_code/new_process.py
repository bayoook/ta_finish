import json
from datetime import date
from itertools import groupby
from time import sleep
import time
from statistics import stdev
from pymongo import MongoClient
from pprint import pprint
import linecache
import sys


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))
    
def hitung(data, data_all, k):
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
    data['fast'] = smoothed
    smoothed = sum([x['fast'] for x in data_all[k][-3:]]) / len(
        [x['fast'] for x in data_all[k][-3:]])
    data['smooth'] = smoothed

    #ema
    try:
        eman = [x for x in data_all[k][-2]['ema']]
    except:
        eman = [0, 0, 0, 0, 0]
    ema5 = ((data['close'] - eman[0]) * (2 / (len(data_all[k][-5:]) + 1))) + (eman[0])
    ema10 = ((data['close'] - eman[1]) * (2 / (len(data_all[k][-10:]) + 1))) + (eman[1])
    ema20 = ((data['close'] - eman[2]) * (2 / (len(data_all[k][-20:]) + 1))) + (eman[2])
    ema50 = ((data['close'] - eman[3]) * (2 / (len(data_all[k][-50:]) + 1))) + (eman[3])
    ema100 = ((data['close'] - eman[4]) * (2 / (len(data_all[k][-100:]) + 1))) + (
    eman[4])
    # eman = ema
    data['ema'] = [ema5, ema10, ema20, ema50, ema100]
    # print(data['ema'])
    # exit(1)
    # SES
    try:
        ses = data_all[k][-2]['ema'][3]
    except:
        ses = float(data["avg"])
    ses_fin = ses + 0.1 * (c - ses)
    ses = ses_fin
    data['ses'] = ses_fin

    # Boolinger Band
    # print(data_all[k][-20:])
    tp = [(x['high'] + x['low'] + x['close']) / 3 for x in data_all[k]]
    sma5 = sum(tp[-5:]) / len(tp[-5:])
    sma10 = sum(tp[-10:]) / len(tp[-10:])
    sma20 = sum(tp[-20:]) / len(tp[-20:])
    sma50 = sum(tp[-50:]) / len(tp[-50:])
    sma100 = sum(tp[-100:]) / len(tp[-100:])

    m = 2
    data['sma'] = [sma5, sma10, sma20, sma50, sma100]
    try:
        std = stdev(tp[-20:])
    except:
        std = 0
    up = data['sma'][2] + (m * std)
    lo = data['sma'][2] - (m * std)
    data['bol_hi'] = up
    data['bol_lo'] = lo
    # print(data['sma'])
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
    # if float(data["ses"]) >= float(data["close"]):
    #     data['ses_stat'] = 1
    #     # print("ses sell")
    # else:
    #     data['ses_stat'] = 2
    data['ses_stat'] = 1 if float(data["ses"]) >= float(data["close"]) else 2
    # print("ses buy")
    # End SES
    # EMA
    data['ema_stat'] = [1 if x >= data['close'] else 2 for x in
                        data['ema']]
    data['sma_stat'] = [1 if x >= data['close'] else 2 for x in
                        data['sma']]
    # if float(data["ema"]) < float(data["avg"]):
    #     data['ema_stat'] = 1
    #     # print("ema sell")
    # elif float(data["ema"]) > float(data["avg"]):
    #     data['ema_stat'] = 2
    # else:
    #     data['ema_stat'] = 0

    # exit(1)
    # print("ema buy")
    # End EMA
    # Stochastic
    # 1 smooth > fast, 2 fast < smooth, 0 start
    if (statusk == 1 and data["smooth"] <= data['fast']) or (
            statusk == 0 and data['fast'] <= data['smooth']):
        statusk = 1 if data["smooth"] >= data['fast'] else 0
        if float(data["smooth"]) > float(80):
            data['sto_stat'] = 1
            # print("sto sell")
        elif float(data["smooth"]) < float(20):
            data['sto_stat'] = 2
        else:
            data['sto_stat'] = 0
    else:
        data['sto_stat'] = 0
    # print("sto buy")

    try:
        ro = open('order_' + datetime_today + fFoot, 'r')
        so = ro.read().splitlines()
        ro.close()
    except Exception as e:
        so = ['']
    ro = open('data/order/order_' + datetime_today + fFoot, 'a')
    if data['sto_stat'] == data['bol_stat'] == data['ses_stat'] == data[
        'ema_stat'] == 1:
        data['status'] = '1'
        value_save = str(k + ' ' + str(data['status']) + ' ' + data['time'])
        # print(value_save)
        if value_save not in so:
            ro.write(value_save + '\n')
    elif data['sto_stat'] == data['bol_stat'] == data['ses_stat'] == data[
        'ema_stat'] == 2:
        data['status'] = '2'
        value_save = str(k + ' ' + str(data['status']) + ' ' + data['time'])
        # print(value_save)
        if value_save not in so:
            ro.write(value_save + '\n')
    else:
        data['status'] = '0'
    ro.close()
    return data

def olah(x, waktu):
    client = MongoClient()
    db = client['dataSaham']

    data_k = []
    minus_day = 1 if date.today().strftime("%A") == 'Saturday' else 2 if date.today().strftime("%A") == 'Sunday' else 0
    minus_yesterday = 3 if date.today().strftime("%A") == 'Monday' else 1
    minus_day = x
    plus = 0
    minus = 1 if x < 0 else 0
    day = f"{date.today().day - minus_day + plus:02d}"
    month = str(f"{date.today().month - minus:02d}")
    year = f"{date.today().year:02d}"
    datetime_today = str(day) + month + year
    fHead = "live_trade_"
    fFoot = ".txt"
    fOlah_today = fHead + datetime_today + fFoot
    data_dir = 'data/'
    live_dir = 'live/'
    print(datetime_today)
    time_sudah = ""
    while 1:
        try:
            file = open(data_dir + live_dir + fOlah_today, 'r')
            break
        except Exception as e:
            print(e)
            sleep(100)
            pass
    x10 = []
    now = None
    o = 1
    db.data.remove({'date': datetime_today, 'period': waktu})
    print('get data 5 days before')
    a = [x for x in db.data.find({"period":1}).distinct('date')[-5:]]
    name = ''
    data_all = {}
    ddd = []
    print(a)
    cursor_ = db.data.find({"$or":[{'date':x, 'period': waktu} for x in a]}).sort('_id', 1)
    for key in cursor_:
        try:
            if key['name'] not in data_all:
                data_all[key['name']] = []
            if len(data_all[key['name']]) >= 200:
                data_all[key['name']].pop(0)
            data_all[key['name']].append(key['data'])
        except Exception as e:
            print(e)
            pass
    print('processing date today')
    try:
        wait = 0
        while 1:
            where = file.tell()
            line = file.readline().replace('\'', '"')
            if not line:
                file.seek(where)
                wait += 1
                sleep(1)
            wait = 0 if line else wait
            time_sudah = "" if line else time_sudah
            if line or wait == 60:
                try:
                    if wait == 60:
                        try:
                            x10[-1]['time'] = x10[-1]['time'].split(':')[0] + ":" + str(
                                int(x10[-1]['time'].split(':')[1]) + 1) + ":" + x10[-1]['time'].split(':')[2]
                            line = json.dumps(x10[-1])
                            if x10[-1]['time'].split(':')[0] + ":" + str(
                                    int(x10[-1]['time'].split(':')[1]) + 1) != time_sudah:
                                time_sudah = x10[-1]['time'].split(':')[0] + ":" + str(
                                    int(x10[-1]['time'].split(':')[1]) + 1)
                            else:
                                continue
                        except:
                            PrintException
                            wait = 0
                            pass
                    x = json.loads(line)
                    x['ts'] = x['time'].split(':')[:-1]
                    x['ts'][1] = (int(int(x['ts'][1]) / waktu))
                    if now is None:
                        now = x['ts'][1]
                    if x['ts'][1] != now or wait == 60:
                        if wait == 60:
                            now = x['ts'][1]
                            x10[-1]['time'] = x10[-1]['time'].split(':')[0] + ":" + str(
                                int(x10[-1]['time'].split(':')[1]) - 1) + ":" + x10[-1]['time'].split(':')[2]
                        try:
                            print(x10[-1]['time'], len(x10))
                        except:
                            print(x10[0]['time'], len(x10))
                        saham_list = x10
                        data_s = []
                        fast_per = []
                        smooth_per = []
                        ope = []
                        eman = 0
                        ses = 0
                        statusk = 0
                        saham_list.sort(key=lambda y: y['stock'])
                        i = 0
                        arr_ = []
                        for k, v in groupby(saham_list, key=lambda y: y['stock']):
                            lst = list(v)
                            k1 = lst[0]['time'][:5]
                            time_data = time.mktime(time.strptime(datetime_today + ' ' + k1, '%d%m%Y %H:%M'))
                            price = [int(p['price'].replace(',', '')) for p in lst]
                            vol = sum([int(p['vol'].replace(',', '')) * 100 for p in lst])
                            sum_price = sum(
                                [int(p['price'].replace(',', '')) * (int(p['vol'].replace(',', '')) * 100) for p in
                                 lst])
                            try:
                                data = {
                                    'time': time_data * 1000,
                                    'high': max(price),
                                    'low': min(price),
                                    'open': price[0],
                                    'close': price[-1],
                                    'vol': vol,
                                    'sum': sum_price,
                                    'avg': sum_price / vol,
                                }
                                try:
                                    data_all[k].append(data)
                                except:
                                    data_all[k] = []
                                    data_all[k].append(data)
                                if data != {}:
                                    data = hitung(data, data_all, k)
                                data_all[k].pop(0)
                                data_all[k].pop(-1)
                                data_all[k].append(data)
                                arr_.append({
                                    "date": datetime_today,
                                    "name": k,
                                    "period": waktu,
                                    "data": data
                                })
                            except Exception as e:
                                print("Error", e, "at", k, k1, vol)
                                PrintException()
                        try:
                            db.data.insert_many(
                                arr_
                            )
                        except Exception as e:
                            print(e)
                            PrintException()
                        if wait == 0:
                            now = x['ts'][1]
                            x10.clear()
                            x10.append(x)
                        if wait == 60:
                            x10.clear()
                            # return 0
                    else:
                        x10.append(x)
                        now = x['ts'][1]
                except Exception as e:
                    print("error", e)
                    PrintException()
    except Exception as e:
        print('closed ', e)


# xx = [-3, -5, -8, -9, -10, -11, -12, -15, -16, -17, -18, -19, -22, -23, -24, -25, -26, 1]
# xx = [17]
# for x in xx:
#     olah(x, int(sys.argv[1]))
try:
    while 1:
        olah(0, 1)
except Exception as e:
    print(e)
    PrintException()