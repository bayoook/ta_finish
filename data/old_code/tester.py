from datetime import datetime as date
import json
from statistics import stdev

def newstream(saham, periode):
    periode = int(periode)
    saham = str(saham)
    if date.today().strftime("%A") == 'Saturday':
        day = int(f"{date.today().day:02d}") - 1
        month = f"{date.today().month:02d}"
        year = f"{date.today().year:02d}"
    elif date.today().strftime("%A") == 'Sunday':
        day = int(f"{date.today().day:02d}") - 2
        month = f"{date.today().month:02d}"
        year = f"{date.today().year:02d}"
    else:
        day = int(f"{date.today().day:02d}")
        month = f"{date.today().month:02d}"
        year = f"{date.today().year:02d}"

    datetime_today = str(day) + month + year
    datetime_yesterday = str(day - 1) + month + year
    fHead = "olah_"
    fFoot = ".txt"
    fName = fHead + str(day) + month + year + fFoot
    fOlah_today = fHead + datetime_today + fFoot
    fOlah_yesterday = fHead + datetime_yesterday + fFoot
    print(fOlah_today)
    print(fOlah_yesterday)

    def read_kemarin():
        return_array = []
        file = open(fOlah_yesterday, 'r')
        lines = file.readlines()
        h_s = 9
        data_s = []
        for line in lines:
            data = json.loads(line.replace("'", '"'))
            ret_d = {}
            count_time = 0
            if data['stock'] == saham:
                if periode == 1:
                    ret_d = data
                else:
                    if count_time == 0:
                        count_time = int(int(data['time'].split(':')[1]) / periode) + 1
                        if count_time == 0:
                            count_time = 1
                    data_s.append(data)
                    print(count_time)
                    try:
                        if int(data['time'].split(':')[1]) >= periode * count_time:
                            data_s = data_s[:-1]
                            ret_d = hitung_data(data_s, count_time * periode)
                            data_s.clear()
                            data_s.append(data)
                            count_time += 1
                        if int(data['time'].split(':')[0]) != h_s:
                            data_s = data_s[:-1]
                            ret_d = hitung_data(data_s, count_time * periode)
                            data_s.clear()
                            data_s.append(data)
                            count_time = int(int(data['time'].split(':')[1]) / periode) + 1
                            h_s = int(data['time'].split(':')[0])
                    except Exception as e:
                        print('Error exception ', e)
                return_array.append(ret_d)
        return return_array

    def sendData():
        file = open(fOlah_today, 'r')
        try:
            count_time = 0
            h_s = 9
            data_s = []
            c = 0
            fast_per = []
            smooth_per = []
            av = 0
            ope = []
            eman = 0
            ses = 0

            # 1 smooth > fast, 2 fast < smooth, 0 start
            statusk = 0
            arr_new = read_kemarin()
            # print(arr_new)
            while 1:
                where = file.tell()
                line = file.readline().replace('\'', '"')
                if not line:
                    file.seek(where)
                else:
                    try:
                        data = json.loads(line)
                        ret_d = {}
                        if data['stock'] == saham:
                            if periode == 1:
                                ret_d = data
                            else:
                                if count_time == 0:
                                    count_time = int(int(data['time'].split(':')[1]) / periode) + 1
                                    if count_time == 0:
                                        count_time = 1
                                data_s.append(data)
                                try:
                                    if int(data['time'].split(':')[1]) >= periode * count_time:
                                        data_s = data_s[:-1]
                                        ret_d = hitung_data(data_s, count_time * periode)
                                        data_s.clear()
                                        data_s.append(data)
                                        count_time += 1
                                    if int(data['time'].split(':')[0]) != h_s:
                                        data_s = data_s[:-1]
                                        ret_d = hitung_data(data_s, count_time * periode)
                                        data_s.clear()
                                        data_s.append(data)
                                        count_time = int(int(data['time'].split(':')[1]) / periode) + 1
                                        h_s = int(data['time'].split(':')[0])
                                except Exception as e:
                                    print('Error exception ', e)
                            if c != 0 and av != 0 and ret_d != {}:
                                arr_new.append(ret_d)
                                av = float(ret_d["avg"])
                                c = int(ret_d["close"])

                                # Stochastic
                                # exit(1)
                                low = min([x['low'] for x in arr_new[-14:]])
                                high = max([x['high'] for x in arr_new[-14:]])
                                fast_line = ((c - low) / (high - low)) * 100
                                # ret_d['fast'] = fast_line
                                fast_per.append(float(fast_line))
                                # if len(fast_per) >= 1:
                                smoothed = sum(fast_per[-3:]) / len(fast_per[-3:])
                                smooth_per.append(smoothed)
                                ret_d['fast'] = smoothed
                                # if len(smooth_per) >= 1:
                                smoothed = sum(smooth_per[-3:]) / len(smooth_per[-3:])
                                smooth_per.append(smoothed)
                                ret_d['smooth'] = smoothed
                                # EMA
                                ope.append(int(ret_d["open"]))
                                ema = ((c - eman) * (2 / (len(ope[-10:]) + 1))) + eman
                                eman = ema
                                av = float(ret_d["avg"])
                                ret_d['ema'] = ema

                                # SES
                                if ses == 0:
                                    ses = float(ret_d["avg"])
                                ses_fin = ses + 0.1 * (c - ses)
                                ses = ses_fin
                                ret_d['ses'] = ses_fin

                                # Boolinger Band
                                tp = [(x['high'] + x['low'] + x['close']) / 3 for x in arr_new[-20:]]
                                sma = sum(tp) / len(tp)

                                m = 2
                                std = stdev(tp)
                                up = sma + m * std
                                lo = sma - m * std

                                ret_d['bol_hi'] = up
                                ret_d['bol_lo'] = lo
                                ret_d['sma'] = sma
                                # End of Boolinger Band

                                # 1 == sell, 2 == buy
                                # Bollinger
                                if float(ret_d["high"]) > float(ret_d["bol_hi"]) \
                                        or float(ret_d["open"]) > float(ret_d["bol_hi"]) \
                                        or float(ret_d["close"]) > float(ret_d["bol_hi"]) \
                                        or float(ret_d["low"]) > float(ret_d["bol_hi"]):
                                    ret_d['bol_stat'] = 1
                                elif float(ret_d["high"]) < float(ret_d["bol_lo"]) \
                                        or float(ret_d["open"]) < float(ret_d["bol_lo"]) \
                                        or float(ret_d["close"]) < float(ret_d["bol_lo"]) \
                                        or float(ret_d["low"]) < float(ret_d["bol_lo"]):
                                    ret_d['bol_stat'] = 2
                                else: ret_d['bol_stat'] = 0
                                # End Bol
                                # SES
                                if float(ret_d["ses"]) < float(ret_d["avg"]):
                                    ret_d['ses_stat'] = 1
                                    # print("ses sell")
                                elif float(ret_d["ses"]) > float(ret_d["avg"]):
                                    ret_d['ses_stat'] = 2
                                else: ret_d['ses_stat'] = 0
                                    # print("ses buy")
                                # End SES
                                # EMA
                                if float(ret_d["ema"]) < float(ret_d["avg"]):
                                    ret_d['ema_stat'] = 1
                                    # print("ema sell")
                                elif float(ret_d["ema"]) > float(ret_d["avg"]):
                                    ret_d['ema_stat'] = 2
                                else: ret_d['ema_stat'] = 0
                                    # print("ema buy")
                                # End EMA
                                # Stochastic
                                # 1 smooth > fast, 2 fast < smooth, 0 start
                                if (statusk == 1 and ret_d["smooth"] < ret_d['fast']) \
                                        or (statusk == 0 and ret_d['fast'] < ret_d['smooth']):
                                    statusk = 1 if ret_d["smooth"] >= ret_d['fast'] else 0
                                    if float(ret_d["smooth"]) > float(80):
                                        ret_d['sto_stat'] = 1
                                        # print("sto sell")
                                    elif float(ret_d["smooth"]) < float(20):
                                        ret_d['sto_stat'] = 2
                                    else:
                                        ret_d['sto_stat'] = 0
                                else: ret_d['sto_stat'] = 0
                                    # print("sto buy")
                                try:
                                    ro = open('order_' + datetime_today + fFoot, 'r')
                                    so = ro.read().splitlines()
                                    ro.close()
                                except:
                                    so = ['']
                                ro = open('order_' + datetime_today + fFoot, 'a')
                                if ret_d['sto_stat'] == ret_d['bol_stat'] == ret_d['ses_stat'] == ret_d['ema_stat'] == 1:
                                    ret_d['status'] = 1
                                    value_save = ret_d['stock'] + ' ' + str(ret_d['status']) + ' ' + ret_d['time']
                                    # print(ret_d['time'] + ":sell")
                                    # print(value_save)
                                    # print(so)
                                    if value_save not in so:
                                        ro.write(value_save + '\n')
                                elif ret_d['sto_stat'] == ret_d['bol_stat'] == ret_d['ses_stat'] == ret_d['ema_stat'] == 2:
                                    ret_d['status'] = 2
                                    value_save = ret_d['stock'] + ' ' + str(ret_d['status']) + ' ' + ret_d['time']
                                    # print(ret_d['time'] + ":Buy")
                                    # print(value_save)
                                    # print(so)
                                    if value_save not in so:
                                        ro.write(value_save + '\n')
                                else: ret_d['status'] = 0
                                ro.close()
                            elif ret_d != {}:
                                c = int(ret_d["close"])
                                av = float(ret_d["avg"])
                            # print(ret_d)
                        try:
                            if ret_d != 0 and ret_d != {}:
                                x = "data: " + json.dumps(ret_d) + "\n\n"
                        except Exception as e:
                            print('Error exception ', e)
                            # exit(1)
                    except Exception as e:
                        print('Error exception ', e)
        except Exception as e:
            print('Error exception ', e)

    def hitung_data(data, waktu):
        jss = {}
        if len(data) == 0:
            print(waktu)
            return {}
        else:
            jss['time'] = data[0]['time'].split(':')[0] + ':' + str(waktu)
            if waktu == 60:
                jss['time'] = str(int(data[0]['time'].split(':')[0]) + 1) + ':00'
            jss['stock'] = data[0]['stock']
            jss['high'] = max(max(x['high'] for x in data), max(x['low'] for x in data))
            jss['low'] = min(min(x['high'] for x in data), min(x['low'] for x in data))
            jss['open'] = data[0]['open']
            try:
                jss['close'] = data[-1]['close']
            except:
                jss['close'] = data[0]['close']
            jss['vol'] = sum(int(x['vol']) for x in data)
            jss['avg'] = str(sum(float(x['avg']) * int(x['vol']) for x in data) / sum(int(x['vol']) for x in data))
        return jss

    return sendData()

import sys

newstream(sys.argv[2], sys.argv[1])

