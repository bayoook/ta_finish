import json
from datetime import date
from itertools import groupby
from time import sleep
from statistics import stdev
from pymongo import MongoClient
from pprint import pprint
import sys
import os
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


def olah(d, md):
    client = MongoClient()
    db = client['stock-data']
    minus_day = 1 if date.today().strftime("%A") == 'Saturday' else 2 if date.today().strftime("%A") == 'Sunday' else 0
    minus_yesterday = 3 if date.today().strftime("%A") == 'Monday' else 1
    day = f"{date.today().day - minus_day:02d}"
    try:
        day = f"{int(d):02d}"
        minus_yesterday = int(md)
    except Exception as e:
        print('day', e)
        PrintException()
        pass
    month = str(int(f"{date.today().month:02d}"))
    year = f"{date.today().year:02d}"
    datetime_today = str(day) + month + year
    day_y = f"{int(day) - minus_yesterday:02d}"
    datetime_yesterday = str(day_y) + month + year
    print(datetime_today)
    print(datetime_yesterday)
    fHead = "live_trade_"
    fFoot = ".txt"
    fOlah_today = fHead + datetime_today + fFoot
    fOlah_yesterday = fHead + datetime_yesterday + fFoot
    statusk = 0
    data_dir = 'data/'
    live_dir = 'live/'
    while 1:
        try:
            file = open(data_dir + live_dir + fOlah_today, 'r')
            break
        except Exception as e:
            print('error', e)
            PrintException()
            sleep(100)
            pass
    x10 = []
    now = None
    waktu = 1
    o = 1
    cursor_ = db.stocks.find(
        {"date": datetime_yesterday}
    )

    name = ''
    data_all = {}
    for key in cursor_:
        kds = key['data']
        for kd in kds:
            try:
                data_all[name]
            except Exception as e:
                print('b')
                PrintException()
            name = kd['name']
            data = kd['data']
            data_all[name] = data
    db.stocks.delete_one({'date': datetime_today})
    db.stocks.insert_one({
        "date": datetime_today,
        "data": []
    })
    try:
        data_k = []
        data_s = []
        fast_per = []
        smooth_per = []
        ope = []
        eman = 0
        ses = 0
        data_file = file.read().replace("'", '"').splitlines()
        saham_list = []

        for x in data_file:
            x = json.loads(x)
            saham_list.append(x)
        try:
            # saham_list = [json.loads(x) for x in data_file]
            saham_list.sort(key=lambda y: y['stock'])
            for k, v in groupby(saham_list, key=lambda y: y['stock']):
                arr_ = []
                ret_d = {}
                # data_all[k] = []
                lst = list(v)
                lst.sort(key=lambda y: y['time'][:5])
                if k not in data_k:
                    db.stocks.update_one(
                        {"date": datetime_today},
                        {"$push": {
                            "data": {
                                "name": k,
                                "data": []
                            }
                        }}
                    )
                    data_k.append(k)
                for k1, v1 in groupby(lst, key=lambda y: y['time'][:5]):
                    lst1 = list(v1)
                    price = [int(p['price'].replace(',', '')) for p in lst1]
                    vol = sum([int(p['vol'].replace(',', '')) * 100 for p in lst1])
                    sum_price = sum(
                        [int(p['price'].replace(',', '')) * (int(p['vol'].replace(',', '')) * 100) for p in
                         lst1])
                    try:
                        data = {
                            'time': k1,
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
                            data['fast'] = smoothed
                            smoothed = sum([x['fast'] for x in data_all[k][-3:]]) / len(
                                [x['fast'] for x in data_all[k][-3:]])
                            data['smooth'] = smoothed

                            # EMA
                            try:
                                # eman = data_all[k][-2]['ema']
                                eman = [x for x in data_all[k][-2]['ema']]
                            except:
                                eman = [0, 0, 0, 0, 0]
                            ema5 = ((data['close'] - eman[0]) * (2 / (5 + 1))) + (eman[0]) if len(
                                data_all[k]) >= 5 else 0
                            ema10 = ((data['close'] - eman[1]) * (2 / (10 + 1))) + (eman[1]) if len(
                                data_all[k]) >= 10 else 0
                            ema20 = ((data['close'] - eman[2]) * (2 / (20 + 1))) + (eman[2]) if len(
                                data_all[k]) >= 20 else 0
                            ema50 = ((data['close'] - eman[3]) * (2 / (50 + 1))) + (eman[3]) if len(
                                data_all[k]) >= 50 else 0
                            ema100 = ((data['close'] - eman[4]) * (2 / (100 + 1))) + (eman[4]) if len(
                                data_all[k]) >= 100 else 0
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

                            # sma = sum(tp[:-]) / len(tp)
                            # SMA
                            # 1
                            # sma = sum(tp) / len(tp)
                            # 5
                            # # ope5.append(int(data["open"]))
                            # if len(ope5) > 5:
                            #     ope5.pop(0)
                            sma5 = sum(tp[-5:]) / len(tp[-5:])
                            sma10 = sum(tp[-10:]) / len(tp[-10:])
                            sma20 = sum(tp[-20:]) / len(tp[-20:])
                            sma50 = sum(tp[-50:]) / len(tp[-50:])
                            sma100 = sum(tp[-100:]) / len(tp[-100:])

                            m = 2
                            try:
                                std = stdev(tp)
                            except:
                                std = 0
                            up = sma20 + m * std
                            lo = sma20 - m * std

                            data['bol_hi'] = up
                            data['bol_lo'] = lo
                            data['sma'] = [sma5, sma10, sma20, sma50, sma100]
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
                            if float(data["ses"]) < float(data["avg"]):
                                data['ses_stat'] = 1
                                # print("ses sell")
                            elif float(data["ses"]) > float(data["avg"]):
                                data['ses_stat'] = 2
                            else:
                                data['ses_stat'] = 0
                            # print("ses buy")
                            # End SES
                            # EMA
                            data['ema_stat'] = [1 if x < data['avg'] else 2 if x > data['avg'] else 0 for x in
                                                data['ema']]
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
                        del data_all[k][-1]
                        data_all[k].append(data)
                        arr_.append(data)
                    except Exception as e:
                        print("Error", e, "at", k, k1, vol)
                        PrintException()
                if len(arr_) > 200:
                    print(k, len(arr_), arr_[-1])
                db.stocks.update_one(
                    {"date": datetime_today, "data.name": k},
                    {"$push": {
                        "data.$.data": {
                            "$each": arr_
                        }
                    }}
                )
        except Exception as e:
            print("error", e)
            PrintException()

    except Exception as e:
        print('closed ', e)
        PrintException()


dir_list = os.listdir('data/live/')
dir_list = sorted(dir_list)[1:]
dir_list = [int(x.replace('live_trade_', '').replace('.txt', '')[:2]) for x in dir_list]
for k, x in enumerate(dir_list):
    if k != 0:import json
from datetime import date
from itertools import groupby
from time import sleep
from statistics import stdev
from pymongo import MongoClient
from pprint import pprint
import sys
import os
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


def olah(d, md):
    client = MongoClient()
    db = client['stock-data']
    minus_day = 1 if date.today().strftime("%A") == 'Saturday' else 2 if date.today().strftime("%A") == 'Sunday' else 0
    minus_yesterday = 3 if date.today().strftime("%A") == 'Monday' else 1
    day = f"{date.today().day - minus_day:02d}"
    try:
        day = f"{int(d):02d}"
        minus_yesterday = int(md)
    except Exception as e:
        print('day', e)
        PrintException()
        pass
    month = str(int(f"{date.today().month:02d}"))
    year = f"{date.today().year:02d}"
    datetime_today = str(day) + month + year
    day_y = f"{int(day) - minus_yesterday:02d}"
    datetime_yesterday = str(day_y) + month + year
    print(datetime_today)
    print(datetime_yesterday)
    fHead = "live_trade_"
    fFoot = ".txt"
    fOlah_today = fHead + datetime_today + fFoot
    fOlah_yesterday = fHead + datetime_yesterday + fFoot
    statusk = 0
    data_dir = 'data/'
    live_dir = 'live/'
    while 1:
        try:
            file = open(data_dir + live_dir + fOlah_today, 'r')
            break
        except Exception as e:
            print('error', e)
            PrintException()
            sleep(100)
            pass
    x10 = []
    now = None
    waktu = 1
    o = 1
    cursor_ = db.stocks.find(
        {"date": datetime_yesterday}
    )

    name = ''
    data_all = {}
    for key in cursor_:
        kds = key['data']
        for kd in kds:
            try:
                data_all[name]
            except Exception as e:
                print('b')
                PrintException()
            name = kd['name']
            data = kd['data']
            data_all[name] = data
    db.stocks.delete_one({'date': datetime_today})
    db.stocks.insert_one({
        "date": datetime_today,
        "data": []
    })
    try:
        data_k = []
        data_s = []
        fast_per = []
        smooth_per = []
        ope = []
        eman = 0
        ses = 0
        data_file = file.read().replace("'", '"').splitlines()
        saham_list = []

        for x in data_file:
            x = json.loads(x)
            saham_list.append(x)
        try:
            # saham_list = [json.loads(x) for x in data_file]
            saham_list.sort(key=lambda y: y['stock'])
            for k, v in groupby(saham_list, key=lambda y: y['stock']):
                arr_ = []
                ret_d = {}
                # data_all[k] = []
                lst = list(v)
                lst.sort(key=lambda y: y['time'][:5])
                if k not in data_k:
                    db.stocks.update_one(
                        {"date": datetime_today},
                        {"$push": {
                            "data": {
                                "name": k,
                                "data": []
                            }
                        }}
                    )
                    data_k.append(k)
                for k1, v1 in groupby(lst, key=lambda y: y['time'][:5]):
                    lst1 = list(v1)
                    price = [int(p['price'].replace(',', '')) for p in lst1]
                    vol = sum([int(p['vol'].replace(',', '')) * 100 for p in lst1])
                    sum_price = sum(
                        [int(p['price'].replace(',', '')) * (int(p['vol'].replace(',', '')) * 100) for p in
                         lst1])
                    try:
                        data = {
                            'time': k1,
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
                            data['fast'] = smoothed
                            smoothed = sum([x['fast'] for x in data_all[k][-3:]]) / len(
                                [x['fast'] for x in data_all[k][-3:]])
                            data['smooth'] = smoothed

                            # EMA
                            try:
                                # eman = data_all[k][-2]['ema']
                                eman = [x for x in data_all[k][-2]['ema']]
                            except:
                                eman = [0, 0, 0, 0, 0]
                            ema5 = ((data['close'] - eman[0]) * (2 / (5 + 1))) + (eman[0]) if len(
                                data_all[k]) >= 5 else 0
                            ema10 = ((data['close'] - eman[1]) * (2 / (10 + 1))) + (eman[1]) if len(
                                data_all[k]) >= 10 else 0
                            ema20 = ((data['close'] - eman[2]) * (2 / (20 + 1))) + (eman[2]) if len(
                                data_all[k]) >= 20 else 0
                            ema50 = ((data['close'] - eman[3]) * (2 / (50 + 1))) + (eman[3]) if len(
                                data_all[k]) >= 50 else 0
                            ema100 = ((data['close'] - eman[4]) * (2 / (100 + 1))) + (eman[4]) if len(
                                data_all[k]) >= 100 else 0
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

                            # sma = sum(tp[:-]) / len(tp)
                            # SMA
                            # 1
                            # sma = sum(tp) / len(tp)
                            # 5
                            # # ope5.append(int(data["open"]))
                            # if len(ope5) > 5:
                            #     ope5.pop(0)
                            sma5 = sum(tp[-5:]) / len(tp[-5:])
                            sma10 = sum(tp[-10:]) / len(tp[-10:])
                            sma20 = sum(tp[-20:]) / len(tp[-20:])
                            sma50 = sum(tp[-50:]) / len(tp[-50:])
                            sma100 = sum(tp[-100:]) / len(tp[-100:])

                            m = 2
                            try:
                                std = stdev(tp)
                            except:
                                std = 0
                            up = sma20 + m * std
                            lo = sma20 - m * std

                            data['bol_hi'] = up
                            data['bol_lo'] = lo
                            data['sma'] = [sma5, sma10, sma20, sma50, sma100]
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
                            if float(data["ses"]) < float(data["avg"]):
                                data['ses_stat'] = 1
                                # print("ses sell")
                            elif float(data["ses"]) > float(data["avg"]):
                                data['ses_stat'] = 2
                            else:
                                data['ses_stat'] = 0
                            # print("ses buy")
                            # End SES
                            # EMA
                            data['ema_stat'] = [1 if x < data['avg'] else 2 if x > data['avg'] else 0 for x in
                                                data['ema']]
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
                        del data_all[k][-1]
                        data_all[k].append(data)
                        arr_.append(data)
                    except Exception as e:
                        print("Error", e, "at", k, k1, vol)
                        PrintException()
                if len(arr_) > 200:
                    print(k, len(arr_), arr_[-1])
                db.stocks.update_one(
                    {"date": datetime_today, "data.name": k},
                    {"$push": {
                        "data.$.data": {
                            "$each": arr_
                        }
                    }}
                )
        except Exception as e:
            print("error", e)
            PrintException()

    except Exception as e:
        print('closed ', e)
        PrintException()

dir_list = os.listdir('data/live/')
dir_list = sorted(dir_list)[1:]
dl = []
for x in dir_list:
    if os.path.getsize('data/live/' + x) != 0:
        dl.append(x)

dir_list = dl
dir_list = [int(x.replace('live_trade_', '').replace('.txt', '')[:2]) for x in dir_list]

for k, x in enumerate(dir_list):
    if k != 0:
        md = x - dir_list[k-1]
    else:
        md = 1
    olah(x, md)


