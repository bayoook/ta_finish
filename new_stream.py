from flask import Flask, Response, render_template, redirect, jsonify
from datetime import datetime as date
from datetime import timedelta, datetime
from multiprocessing.pool import ThreadPool
import json
from time import sleep
from statistics import stdev
from pymongo import MongoClient
import sys
from pprint import pprint
from flask_pymongo import PyMongo

context = ('/root/certs/min4tozaki.me.crt', '/root/certs/min4tozaki.me.key')

app = Flask(__name__, template_folder='/root/ta/staticweb', static_folder='/root/ta/staticweb', static_url_path='')
port = sys.argv[1]
app.config["MONGO_URI"] = "mongodb://localhost:27017/dataSaham"
client = MongoClient()
mongo = PyMongo(app)
db = client['dataSaham']


@app.route('/')
def default_web():
    return render_template('index.html')


@app.route('/portofolio')
def portof_web():
    return render_template('index_portof.html')


@app.route('/tubes-ml')
def tubes_ml():
    # return 'xyz'
    return redirect('https://colab.research.google.com/drive/1pspjkiI2K8Z1iEcwO1v25u_wkZNqxeJw')


@app.route('/pQw22z/api/<saham>/<tanggal>/<period>/reqAPI', methods=['GET'])
def api_resp(saham, tanggal, period):
    periode = int(period)
    col_name = 'data'
    if periode != 1:
        col_name += period
    saham = str(saham.upper())

    def read_close(saham, period, dy):
        cursor = db[col_name].find({'date': dy, 'name': saham, 'period': int(period)}).sort('_id', -1).limit(1)[0][
            'data']
        print('done read close')
        return cursor

    def read_today(saham, period, tanggal):
        data_all = []
        cursor = db[col_name].find({'date': tanggal, 'name': saham, 'period': int(period)})
        for x in cursor:
            data_all.append(x['data'])
        return data_all

    def read_data(saham, tanggal, period):
        data_all = []
        read_close(saham, period, tanggal)
        pool = ThreadPool(processes=2)
        day = datetime.strptime(tanggal, '%d%m%Y').strftime("%A")
        minus_day = 1 if day == 'Saturday' else 2 if day == 'Sunday' else 0
        dy = (datetime.strptime(tanggal, '%d%m%Y') - timedelta(days=minus_day + 1)).strftime('%d%m%Y')
        result = pool.apply_async(read_close, (saham, period, dy))
        result2 = pool.apply_async(read_today, (saham, period, tanggal))
        print('read done')
        data_all = result2.get()
        print(len(data_all))
        return data_all[:-1]

    return str(read_data(saham, tanggal, period)).replace("'", '"')


@app.route('/firzayusril/api/<tanggal>/<saham>/reqAPI', methods=['GET'])
def api_firza(tanggal, saham):
    period = 1
    saham = str(saham.upper())

    def read_close(saham, period, dy):
        cursor = db[col_name].find({'date': dy, 'name': saham, 'period': int(period)}).sort('_id', -1).limit(1)[0][
            'data']
        print('done read close')
        return cursor

    def read_today(saham, period, tanggal):
        data_all = []
        cursor = db[col_name].find({'date': tanggal, 'name': saham, 'period': int(period)})
        for x in cursor:
            data_all.append(x['data'])
        return data_all

    def read_data(saham, tanggal, period):
        data_all = []
        read_close(saham, period, tanggal)
        pool = ThreadPool(processes=2)
        day = datetime.strptime(tanggal, '%d%m%Y').strftime("%A")
        minus_day = 1 if day == 'Saturday' else 2 if day == 'Sunday' else 0
        dy = (datetime.strptime(tanggal, '%d%m%Y') - timedelta(days=minus_day + 1)).strftime('%d%m%Y')
        # result = pool.apply_async(read_close, (saham, period, dy))
        result2 = pool.apply_async(read_today, (saham, period, tanggal))
        print('read done')
        data_all = result2.get()
        print(len(data_all))
        for x in data_all[:-1]:
            x = str(x)
            yield 'data: ' + x + '\n\n'
            sleep(1)

    return Response(
        read_data(saham, tanggal, period),
        mimetype='text/event-stream')


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
        line = file.read().splitlines()
        if not line:
            file.seek(where)
        else:
            print(line)


@app.route('/<nama_saham>/<waktu_saham>/<tanggal>/live')
def live(nama_saham, waktu_saham, tanggal):
    waktu_saham = int(waktu_saham)
    nama_saham = str(nama_saham.upper())
    periode = waktu_saham
    period = str(waktu_saham)
    col_name = 'data'
    if periode != 1:
        col_name += period
    list_saham = json.loads(open('data/nama_saham', 'r').read())
    nama_full = [x['NamaEmiten'] for x in list_saham if x['KodeEmiten'] == nama_saham][0]
    if nama_saham == 'test':
        return render_template('live_new.html')
    if tanggal == 'today':
        datetime_today = db[col_name].distinct('date')[-1]
        req_live = 'True'
    else:
        datetime_today = tanggal
        req_live = 'False'
    return render_template('live_new.html',
                           saham=nama_saham,
                           nama_full=nama_full,
                           periode=waktu_saham,
                           day=date.today().strftime("%A"),
                           date=datetime_today[2:4] + '-' + datetime_today[:2] + '-' + datetime_today[-4:],
                           tanggal=datetime_today,
                           live=req_live)


@app.route('/<saham>/<periode>/<tanggal>/stream')
def newStream(saham, periode, tanggal):
    periode = int(periode)
    saham = str(saham).upper()
    tanggal = str(tanggal.lower())
    col_name = 'data'
    period = str(periode)
    if periode != 1:
        col_name += period
    if tanggal == 'today':
        datetime_today = db[col_name].find({"period": 1}).distinct('date')[-1]
    else:
        datetime_today = tanggal
    print(datetime_today, saham, periode)

    def readData():
        s = 0
        da = {}
        while 1:
            try:
                cursor = \
                    db[col_name].find({"date": datetime_today, "name": saham, "period": periode}).sort("$natural", -1)[
                        0][
                        'data']
                if cursor != da:
                    yield "data: " + json.dumps(cursor) + '\n\n'
                    if datetime_today != f"{date.today().strftime('%d%m%Y')}":
                        yield "data: DONE-STREAM\n\n"
                        break
                    da = cursor
                else:
                    s += 1
                if s == 1000:
                    s = 0
                    yield "data: KEEP-ALIVE\n\n"
            except Exception as e:
                print(e)
                yield "data: KEEP-ALIVE\n\n"
                sleep(10)
                pass

    return Response(
        readData(),
        mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True, ssl_context=context)
    # app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
