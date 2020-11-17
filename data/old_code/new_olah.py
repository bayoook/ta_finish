import json
from datetime import date
from itertools import groupby
from time import sleep
import sys
from statistics import stdev
from pymongo import MongoClient
from pprint import pprint


def file_name(d=None, m=None, y=None):
    day = f"{date.today().day:02d}"
    month = f"{date.today().month:02d}"
    year = f"{date.today().year:02d}"
    year = y if y else year
    day = d if d else day
    month = m if m else month
    fHead = "live_trade_"
    fHead2 = "olah_new_"
    fFoot = ".txt"
    d = day + month + year
    dy = str(int(day) - 1) + month + year
    fName = fHead + day + month + year + fFoot
    fName2 = fHead2 + day + month + year + fFoot
    return fName, fName2, d, dy


if __name__ == '__main__':
    client = MongoClient()
    db = client['stock-data']
    f1, f2, d, dy = file_name(sys.argv[1], sys.argv[2], sys.argv[3])
    while 1:
        try:
            file = open(f1, 'r')
            break
        except Exception as e:
            print(e)
            sleep(100)
            pass
    x10 = []
    now = 0
    waktu = 1
    o = 1
    # db.stocks.remove({'date': d})
    cursor_ = db.stocks.find(
        {"date": dy}
    )
    name = ''
    data_all = {}
    for key in cursor_:
        kds = key['data']
        for kd in kds:
            try:
                data_all[name]
            except:
                print('a')
            name = kd['name']
            data = kd['data']
            data_all[name] = data
    try:
        data_s = []
        fast_per = []
        smooth_per = []
        ope = []
        eman = 0
        ses = 0
        while 1:
            where = file.tell()
            line = file.readline().replace('\'', '"')
            if not line:
                file.seek(where)
                if sys.argv[1]:
                    print('a')
                    break
            else:
                try:
                    x = json.loads(line)
                    x['ts'] = x['time'].split(':')[:-1]
                    x['ts'][1] = (int(int(x['ts'][1]) / waktu))
                    print(x['ts'])
                    exit(1)
                    if x['ts'][1] != now:
                        saham_list = x10
                        saham_list.sort(key=lambda y: y['stock'])
                        for k, v in groupby(saham_list, key=lambda y: y['stock']):
                            arr_ = []
                            ret_d = {}
                            data_all[k] = []
                            lst = list(v)
                            lst.sort(key=lambda y: y['time'][:5])
                            if db.stocks.count_documents({"date": d}) == 0:
                                db.stocks.insert_one({
                                    "date": d,
                                    "data": []
                                })
                            if db.stocks.count_documents({"date": d, "data.name": k}) == 0:
                                db.stocks.update_one(
                                    {"date": d},
                                    {"$push": {
                                        "data": {
                                            "name": k,
                                            "data": []
                                        }
                                    }}
                                )
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
                                        fast_per.append(float(fast_line))
                                        smoothed = sum(fast_per[-3:]) / len(fast_per[-3:])
                                        smooth_per.append(smoothed)
                                        data['fast'] = smoothed
                                        smoothed = sum(smooth_per[-3:]) / len(smooth_per[-3:])
                                        smooth_per.append(smoothed)
                                        data['smooth'] = smoothed

                                        # EMA
                                        try:
                                            eman = data_all[k][-2]['ema']
                                        except:
                                            eman = 0
                                        ema = ((c - eman) * (2 / (len(data_all[k][-10:]) + 1))) + eman
                                        # eman = ema
                                        data['ema'] = ema

                                        # SES
                                        try:
                                            ses = data_all[k][-2]['ema']
                                        except:
                                            ses = float(data["avg"])
                                        ses_fin = ses + 0.1 * (c - ses)
                                        ses = ses_fin
                                        data['ses'] = ses_fin

                                        # Boolinger Band
                                        tp = [(x['high'] + x['low'] + x['close']) / 3 for x in data_all[k][-20:]]
                                        if len(tp) >= 2:
                                            sma = sum(tp) / len(tp)

                                            m = 2
                                            std = stdev(tp)
                                            up = sma + m * std
                                            lo = sma - m * std

                                            data['bol_hi'] = up
                                            data['bol_lo'] = lo
                                            data['sma'] = sma
                                    print(data)
                                    del data_all[k][-1]
                                    data_all[k].append(data)
                                    db.stocks.update_one(
                                        {"date": d, "data.name": k},
                                        {"$push": {
                                            "data.$.data": data
                                        }}
                                    )
                                except Exception as e:
                                    print("Error", e, "at", k, k1, vol)
                                    pass
                        now = x['ts'][1]
                        x10.clear()
                        x10.append(x)
                    else:
                        x10.append(x)
                        now = x['ts'][1]
                except Exception as e:
                    print("error", e)

    except Exception as e:
        print('closed ', e)

