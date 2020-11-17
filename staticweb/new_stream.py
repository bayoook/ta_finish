from flask import Flask, Response, render_template, redirect
from datetime import datetime as date
import json
from time import sleep
from statistics import stdev
from pymongo import MongoClient
import sys

context = ('/root/certs/min4tozaki.me.crt', '/root/certs/min4tozaki.me.key')

app = Flask(__name__, template_folder='/root/ta/staticweb', static_folder='/root/ta/staticweb', static_url_path='')
# app = Flask(__name__, template_folder='staticweb', static_folder='staticweb', static_url_path='')
port = sys.argv[1]
# port = 80


@app.route('/')
def default_web():
    return render_template('index.html')


@app.route('/status')
def status_jb():
    minus_day = 1 if date.today().strftime("%A") == 'Saturday' else 2 if date.today().strftime("%A") == 'Sunday' else 0
    minus_yesterday = 3 if date.today().strftime("%A") == 'Monday' else 1
    day = int(f"{date.today().day - minus_day:02d}")
    month = str(int(f"{date.today().month:02d}"))
    year = f"{date.today().year:02d}"
    datetime_today = str(day) + month + year
    file = open("order_" + datetime_today + ".txt")
    while 1:
        where = file.tell()
        line = file.readline().replace('\'', '"')
        if not line:
            file.seek(where)
        else:
            print(line)



@app.route('/<nama_saham>/<waktu_saham>/live')
def live(nama_saham, waktu_saham):
    # periode = int(waktu_saham)
    # saham = str(nama_saham)
    # client = MongoClient()
    # db = client['stock-data']
    # minus_day = 1 if date.today().strftime("%A") == 'Saturday' else 2 if date.today().strftime(
    #     "%A") == 'Sunday' else 0
    # minus_yesterday = 3 if date.today().strftime("%A") == 'Monday' else 1
    # minus_day = 11
    # minus_yesterday = 1
    # day = int(f"{date.today().day - minus_day:02d}")
    # month = str(int(f"{date.today().month:02d}"))
    # year = f"{date.today().year:02d}"
    # datetime_today = str(day) + month + year
    # datetime_yesterday = str(day - minus_yesterday) + month + year
    #
    # def read_data():
    #     cursor = db.stocks.find({"date": datetime_today, "data.name": saham}, {"data.$": 1, "data": 1})
    #     # print(datetime_today)
    #     for key in cursor:
    #         data_a = key['data'][0]['data']
    #         return data_a
    nama_saham = nama_saham.upper()
    print(nama_saham)
    # data = read_data()
    # print(data)
    if nama_saham == 'all':
        return "testing"
    else:
        return render_template('live.html',
                               saham=nama_saham,
                               periode=waktu_saham,
                               day=date.today().strftime("%A"))


@app.route('/canvas.js')
def canvas():
    return open('canvas.js', 'r').read()


@app.route('/jquery.js')
def jquery():
    return open('jquery.js', 'r').read()


@app.route('/<saham>/<periode>/data')
def new_stream(saham, periode):
    periode = int(periode)
    saham = str(saham)
    client = MongoClient()
    db = client['stock-data']
    minus_day = 1 if date.today().strftime("%A") == 'Saturday' else 2 if date.today().strftime("%A") == 'Sunday' else 0
    minus_yesterday = 3 if date.today().strftime("%A") == 'Monday' else 1
    day = int(f"{date.today().day - minus_day:02d}")
    month = str(int(f"{date.today().month:02d}"))
    year = f"{date.today().year:02d}"
    datetime_today = str(day) + month + year
    datetime_yesterday = str(day - minus_yesterday) + month + year

    def read_data():
        da = {}
        cursor = db.stocks.find({"date": datetime_today, "data.name": saham}, {"data.$": 1, "data": 1})
        # print(datetime_today)
        for key in cursor:
            data_a = key['data'][0]['data']
            for x in data_a:
                yield "data: " + json.dumps(x) + "\n\n"
            da = data_a[-1]
        while 1:
            cursor = db.stocks.find({"date": datetime_today, "data.name": saham}, {"data.$": 1, "data": 1})
            for key in cursor:
                data_a = key['data'][0]['data']
                if da != data_a[-1]:
                    da = data_a[-1]
                    yield "data: " + json.dumps(data_a[-1]) + "\n\n"
            sleep(1)

    return Response(
        read_data(),
        mimetype='text/event-stream')



@app.route('/<saham>/<periode>/stream')
def newstream(saham, periode):
    periode = int(periode)
    saham = str(saham)

    minus_day = 1 if date.today().strftime("%A") == 'Saturday' else 2 if date.today().strftime("%A") == 'Sunday' else 0
    minus_yesterday = 3 if date.today().strftime("%A") == 'Monday' else 1
    # minus_day = 4
    # minus_yesterday = 1
    day = int(f"{date.today().day - minus_day:02d}")
    month = str(int(f"{date.today().month:02d}"))
    year = f"{date.today().year:02d}"
    datetime_today = str(day) + month + year
    datetime_yesterday = str(day - minus_yesterday) + month + year
    fHead = "olah_"
    fFoot = ".txt"
    fName = fHead + str(day) + month + year + fFoot
    fOlah_today = fHead + datetime_today + fFoot
    fOlah_yesterday = fHead + datetime_yesterday + fFoot
    print(fOlah_today)
    print(fOlah_yesterday)

    def read_kemarin():
        return_array = []
        while 1:
            try:
                file = open(fOlah_yesterday, 'r')
                break
            except Exception as e:
                print(e)
        lines = file.readlines()
        h_s = 9
        data_s = []
        count_time = 0
        for line in lines:
            data = json.loads(line.replace('\'', '"').replace("\n", ""))
            ret_d = {}
            if data['stock'] == saham:
                if periode == 1:
                    ret_d = data
                else:
                    if count_time == 0:
                        # print(data['time'].split(':')[1])
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
                if ret_d != {}:
                    return_array.append(ret_d)
        return return_array

    def sendData():
        while 1:
            try:
                file = open(fOlah_today, 'r')
                break
            except Exception as e:
                # print(e)
                yield "KEEP-ALIVE\n\n"
                sleep(10)
                # pass
        try:
            count_time = 0
            h_s = 9
            data_s = []
            fast_per = []
            smooth_per = []
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
                            if ret_d != {}:
                                arr_new.append(ret_d)
                                av = float(ret_d["avg"])
                                c = int(ret_d["close"])

                                # Stochastic
                                # print(arr_new[-14])
                                # exit(1)
                                low = min([x['low'] for x in arr_new[-14:]])
                                high = max([x['high'] for x in arr_new[-14:]])
                                # print(low, high)
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
                                if (statusk == 1 and ret_d["smooth"] <= ret_d['fast']) or (statusk == 0 and ret_d['fast'] <= ret_d['smooth']):
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
                        else:
                            continue
                        try:
                            if ret_d != 0 and ret_d != {}:
                                yield "data: " + json.dumps(ret_d) + "\n\n"
                        except Exception as e:
                            print('Error exception 1', e)
                            # exit(1)
                    except Exception as e:
                        print('Error exception 2', e)
        except Exception as e:
            print('Error exception 3', e)

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
        # print(jss)
        return jss

    return Response(
        sendData(),
        mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True, ssl_context=context)
    # app.run(host='0.0.0.0', port=80, debug=True, threaded=True)

