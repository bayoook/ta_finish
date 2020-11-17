import requests
import sseclient
from datetime import date, datetime
import schedule
import time
import json


def scrap_graph():
    url_start = open('data/url_graph').read()
    data = requests.get(url_start).text.split(';')
    date_time_today = ""
    for x in data:
        x = x.replace('\n', '')
        if x == 'error':
            print(x)
            time.sleep(1)
            return 0
        if x[:27] == "mapping_data_ke_price[0][0]":
            date_time = time.strptime(x[31:-1], '%Y-%m-%d %H:%M:%S')
            date_time_today = time.strftime("%d%m%Y", date_time)
    file_name = 'data/graph/data_graph_' + date_time_today + '.txt'
    print(file_name)
    f = open(file_name, 'w')
    sahamJSON = json.load(open('data/nama_saham', 'r'))
    p = 0
    for data in sahamJSON:
        k = data['KodeEmiten']
        url_request = url_start.replace('BBNI', k)
        data_saham = requests.get(url_request).text.split(';')
        t = []
        for y, x in enumerate(data_saham):
            if x[:21] == 'mapping_data_ke_price':
                if x[-11:] != 'new Array()':
                    t.append(x.split(' = ')[1])
        try:
            t.pop(0)
        except:
            pass
        i, j = 0, 0
        data = []
        sem = []
        for x in t:
            sem.append(x)
            i += 1
            if i == 7:
                data.append(sem)
                i = 0
                j += 1
                sem = []
        new = []
        for x, y in enumerate(data[:-1]):
            ptime = time.mktime(time.strptime(y[0][1:-1], '%Y-%m-%d %H:%M:%S')) * 1000
            popen = y[1]
            phigh = y[2]
            plow = y[3]
            pclose = y[4]
            pvol = y[5]
            new_data = {
                'saham': k,
                'time': ptime,
                'open': popen,
                'high': phigh,
                'low': plow,
                'close': pclose,
                'vol': pvol,
            }
            f.write(str(new_data) + '\n')
            new.append(new_data)
        print(p, k, 'Done', len(data), 'data parsed')
        p += 1


schedule.every().day.at("20:00").do(scrap_graph)

while True:
    schedule.run_pending()
    time.sleep(1)
