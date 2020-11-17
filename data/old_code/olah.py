from datetime import date
import json
from itertools import groupby
from time import sleep


def olah():
    waktu = 1
    day = f"{date.today().day:02d}"
    month = f"{date.today().month:02d}"
    year = f"{date.today().year:02d}"
    day = "11"
    fHead = "live_trade_"
    fHead2 = "olah_"
    fFoot = ".txt"
    fName = fHead + day + month + year + fFoot
    fName2 = fHead2 + day + month + year + fFoot
    while 1:
        try:
            file = open(fName, 'r')
            ff = open(fName2, 'w')
            break
        except Exception as e:
            print(e)
            sleep(100)
            pass
    x10 = []
    now = 0
    try:
        while 1:
            where = file.tell()
            line = file.readline().replace('\'', '"')
            if not line:
                file.seek(where)
            else:
                try:
                    x = json.loads(line)
                    x['ts'] = x['time'].split(':')[:-1]
                    x['ts'][1] = (int(int(x['ts'][1]) / waktu))
                    if x['ts'][1] != now:
                        saham_list = []
                        saham_list = x10
                        saham_list.sort(key=lambda x: x['stock'])
                        # print(saham_list)
                        for k, v in groupby(saham_list, key=lambda x: x['stock']):
                            lst = list(v)
                            lst.sort(key=lambda x: x['time'][:5])
                            for k1, v1 in groupby(lst, key=lambda x: x['time'][:5]):
                                lst1 = list(v1)
                                price = [int(p['price'].replace(',', '')) for p in lst1]
                                vol = sum([int(p['vol'].replace(',', '')) for p in lst1])
                                sum_price = sum([int(p['price'].replace(',', '')) * int(p['vol'].replace(',','')) for p in lst1])
                                # print(vol)
                                try:
                                    data = {
                                        'stock': k,
                                        'time': k1,
                                        'high': max(price),
                                        'low': min(price),
                                        'open': price[0],
                                        'close': price[-1],
                                        'vol': vol,
                                        'sum': sum_price,
                                        'avg': sum_price / vol,
                                    }
                                    print(k, data['time'])
                                    ff.write(json.dumps(data) + '\n')
                                except Exception as e:
                                    print(k, k1, vol, e)
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
        ff.close()


olah()

