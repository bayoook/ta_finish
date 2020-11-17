import json
from datetime import date, datetime
from itertools import groupby
from time import sleep
import time
from statistics import stdev
from pprint import pprint
from pymongo import MongoClient
import linecache
import sys

client = MongoClient('mongodb://localhost:27017/')
db = client.dataSaham


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


def olah(x, waktu):
    habis_wait = 0
    minus_day = 1 if date.today().strftime("%A") == 'Saturday' else 2 if date.today().strftime("%A") == 'Sunday' else 0
    minus_day = x
    plus = 0
    minus = 1 if x < 0 else 0
    day = str(f"{date.today().day - minus_day + plus:02d}")
    month = str(f"{date.today().month - minus:02d}")
    year = f"{date.today().year:02d}"
    datetime_today = day + month + year
    # datetime_today = '26122019'
    fHead = "live_trade_"
    fFoot = ".txt"
    fOlah_today = fHead + datetime_today + fFoot
    data_dir = 'data/'
    live_dir = 'live/'
    print(fOlah_today)
    time_sudah = ""
    while 1:
        try:
            file = open(data_dir + live_dir + fOlah_today, 'r')
            break
        except Exception as e:
            print(e)
            sleep(100)
            pass

    if len(open(data_dir + live_dir + fOlah_today, 'r').readlines()) == 0:
        print('live trade is not started yet')
        return 'done'
    x10 = []
    now = None
    o = 1
    db.data.remove({'date': datetime_today, 'period': waktu})
    print('get data 5 days before')

    a = [x for x in db.data.find({"period": 1}).distinct('date')]
    a = sorted(a, key=lambda x: datetime.strptime(x, '%d%m%Y'))
    print(x)
    if x != 0:
        a = a[-5 - x:]
    else:
        a = a[-5:]
    name = ''
    data_all = {}
    ddd = []
    print(a)
    # exit(1)
    # exit(1)
    cursor_ = db.data.find({"$or": [{'date': x, 'period': waktu} for x in a]})
    print('done', cursor_.count())
    print('processing date before')
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
    print('done')
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
                    # habis_wait = 0
                    if now is None or habis_wait == 1:
                        now = x['ts']
                        habis_wait = 0

                    if x['ts'] != now or wait == 60:

                        # If losing data
                        # if semen <= 1:
                        #     print('semen', x10[-1]['time'], len(x10))
                        #     semen += 1
                        #     now = x['ts'][1]
                        #     x10.clear()
                        #     x10.append(x)
                        #     continue

                        if wait == 60:
                            now = x['ts']
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
                            if vol == 0:
                                continue
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
                                    smoothed = sum([x['fast'] for x in data_all[k][-3:]]) / len(
                                        [x['fast'] for x in data_all[k][-3:]])
                                    data['smooth'] = smoothed  # Stochastic  Smooth Line
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
                                    ema100 = ((data['close'] - eman[4]) * (2 / (len(data_all[k][-100:]) + 1))) + (
                                    eman[4])
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
                                    up = data['sma'][2] + (m * std)  # Upper Band
                                    lo = data['sma'][2] - (m * std)  # Lower Band
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

                                    if data['bol_stat'] == 1:
                                        sell_signal += 1
                                    elif data['bol_stat'] == 2:
                                        buy_signal += 1

                                    if data['ses_stat'] == 1:
                                        sell_signal += 1
                                    elif data['ses_stat'] == 2:
                                        buy_signal += 1

                                    if data['ema_stat'][2] == 1:
                                        sell_signal += 1
                                    elif data['ema_stat'][2] == 2:
                                        buy_signal += 1

                                    if data['sto_stat'] == 1:
                                        sell_signal += 1
                                    elif data['sto_stat'] == 2:
                                        buy_signal += 1
                                    # Write Predict to file
                                    try:
                                        ro = open('data/order/order_' + datetime_today + fFoot, 'r')
                                        so = ro.read().splitlines()
                                        ro.close()
                                    except Exception as e:
                                        so = ['']
                                    ro = open('data/order/order_' + datetime_today + fFoot, 'a')
                                    if sell_signal >= 3:
                                        data['status'] = '1'
                                        value_save = k + ' ' + str(data['status']) + ' ' + str(
                                            data['time']) + ' ' + str(sell_signal) + ' ' + str(buy_signal) + ' ' + str(
                                            data['open']) + ' ' + str(data['high']) + ' ' + str(
                                            data['low']) + ' ' + str(data['close'])
                                        if value_save not in so:
                                            ro.write(value_save + '\n')
                                    elif buy_signal >= 3:
                                        data['status'] = '2'
                                        value_save = k + ' ' + str(data['status']) + ' ' + str(
                                            data['time']) + ' ' + str(sell_signal) + ' ' + str(buy_signal) + ' ' + str(
                                            data['open']) + ' ' + str(data['high']) + ' ' + str(
                                            data['low']) + ' ' + str(data['close'])
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
                                    "date": datetime_today,
                                    "name": k,
                                    "period": waktu,
                                    "data": data
                                })
                            except Exception as e:
                                print("Error", e, "at", k, k1, vol)
                                PrintException()
                        try:
                            # Inserting array to mongo
                            db.data.insert_many(arr_)
                            # print(now)
                            if now[0] == '16' and now[1] >= 14:
                                return 'done'
                        except Exception as e:
                            print(e)
                            PrintException()

                        if wait == 0:
                            now = x['ts']
                            x10.clear()
                            x10.append(x)
                        if wait == 60:
                            x10.clear()
                            habis_wait = 1
                    else:
                        x10.append(x)
                        now = x['ts']
                except Exception as e:
                    print("error", e)
                    PrintException()
    except Exception as e:
        print('closed ', e)


# xx = [-3, -5, -8, -9, -10, -11, -12, -15, -16, -17, -18, -19, -22, -23, -24, -25, -26, 1]
# xx = [17]
# for x in xx:
#     olah(x, int(sys.argv[1]))

start_olah = 'tdone'
try:
    while 1:
        if start_olah == 'tdone':
            start_olah = olah(0, 1)
            # break
        elif start_olah == 'done':
            try:
                print(datetime.now().strftime('%H%M%S'))
                if datetime.now().strftime('%H') == '09':
                    start_olah = 'tdone'
                    continue
                else:
                    sleep(1)
            except:
                break
except Exception as e:
    print(e)
    PrintException()
