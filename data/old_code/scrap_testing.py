import requests
import pickle
import sseclient
from datetime import date, datetime
import json
import sys
import linecache
import time




url = ''
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))



def get_session(): 
    url = 'http://ipotultima.com'
    session = requests.Session()
    session.head(url)
    r1 = session.get(url)
    angka = r1.url.split('.')[0].replace('https://app','')
    url = 'https://app' + angka +'.ipotindonesia.com/ipot/tablet/'
    print('url =', url)
    return session, url

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
}
gateway_headers = {
    'Cache-Control': 'no-cache',
    'dnt': '1',
    'Sec-Fetch-Mode': 'cors'
}
login_data = {
    'uid': 'username',
    'pwd': 'password',
}
login_pin = {
    'id_menu': 'qlink',
    'uid': 'username',
    'pin': 'pin'
}
lt_data = {
    'p1': '1', 
    'p2': '1114113', 
    'p3': '', 
    'p4': '',
}
# {'header': 'DBS', 'tradetime': '09:00:05', 'sec': 'ACES', 'board': 'RG', 'price': '1,600', 'vol': '1', 'val': '160.0K', 'bycode': 'AT', 'bycodec': '#a858a8', 'bytype': 'D', 'slcode': 'PD', 'slcodec': '#a858a8', 'sltype': 'D', 'tradeno': '669515945', 'byorderno': '1429391902', 'slorderno': '1429414064', 'totdata': '2491', '': ''}
data_ob = {'p1': '1', 'p2': '1114114', 'p3': 'BBCA', 'p4': 'RG', }
file_dbs = 'dbs_' + f"{date.today().strftime('%d%m%Y')}" + '.txt'
f_dbs = open(file_dbs, 'w')
while 1:
    try:
        ps_status = 0
        print('Get session')
        filename = 'data/live/live_trade_' + f"{date.today().strftime('%d%m%Y')}" + '.txt'
        print('datetime_today =', filename.replace('data/live/live_trade_', '').replace('.txt', ''))
        file_portof_c = 'data/portofolio/pc_' + f"{date.today().strftime('%d%m%Y')}" + '.txt'
        file_portof_s = 'data/portofolio/ps_' + f"{date.today().strftime('%d%m%Y')}" + '.txt'
        file_portof_ol = 'data/portofolio/ol_' + f"{date.today().strftime('%d%m%Y')}" + '.txt'
        file_portof_dl = 'data/portofolio/dl_' + f"{date.today().strftime('%d%m%Y')}" + '.txt'
        
        file_else = 'data/else/bs_' + f"{date.today().strftime('%d%m%Y')}" + '.txt'
        f = open(filename, 'a+')
        # f_dbs = open(file_dbs, 'w')
        f_else = open(file_else, 'w')
        print('File save in', filename)
        # exit(1)
        try:
            session, url = get_session()
            session.headers.update(headers)
            
            login = session.post(url + 'submit_login.jsp', data=login_data)
            
            session.get(url + 'ulogout.jsp')
            gateway = session.get(url + 'gateway.jsp', stream=True)
        except Exception as e:
            PrintException()
            print('1', e)
            continue
        
        print('session =', session.cookies)
        with open('session', 'wb') as ff:
            pickle.dump(session.cookies, ff)
        with open('url', 'w') as ff:
            ff.write(url)
        with open('header', 'w') as ff:
            ff.write(str(session.headers))
        
        
        client = sseclient.SSEClient(gateway)

        session.post(url + 'request.jsp', data=lt_data)
        count_ka = 0
        count_nl = 0
        # gateway = session.get(url + 'gateway.jsp', stream=True)
        # exit(1)
        for event in client.events():
            data = event.data
            if data == 'TIMEOUT':
                print('Logged out, trying to logging in')
                break
            elif data == 'KEEP-ALIVE':
                if f"{date.today().strftime('%d%m%Y')}" != filename.replace('data/live/live_trade_', '').replace('.txt', ''):
                    break
                # continue
                if count_ka % 10 == 0:
                    count_ka = 0
                    count_nl += 1
                    print('KEEP-ALIVE')
                if count_nl == 20:
                    print('re request live trade gateway')
                    session.post(url + 'request.jsp', data=lt_data)
                    count_ka = 0
                    count_nl = 0
                count_ka += 1
            elif data == 'UNKNOWN':
                print(data)
            else:
                count_ka = 1
                try:
                    parsed_data = json.loads(data)
                    if parsed_data['header'] == 'LT':
                        # print(parsed_data['time'][:3])
                        f.write(str(parsed_data) + '\n')
                        print('LT', parsed_data['time'], parsed_data['stock'],)
                    elif parsed_data['header'] == 'PS':
                        if ps_status == 0:
                            f_portof_s = open(file_portof_s, 'w')
                            ps_status = 1
                            f_portof_s.write(str(parsed_data) + '\n')
                            f_portof_s.close
                        else:
                            f_portof_s = open(file_portof_s, 'a+')
                            f_portof_s.write(str(parsed_data) + '\n')
                            f_portof_s.close()
                        print('PS', parsed_data['sec'], parsed_data['val'], ps_status)
                    elif parsed_data['header'] == 'PC':
                        f_portof_c = open(file_portof_c, 'w')
                        ps_status = 0
                        f_portof_c.write(str(parsed_data) + '\n')
                        # f_portof_c.close()
                        print('PC', parsed_data['aname'])
                    # elif parsed_data['header'] != 'OB' and  parsed_data['header'] != 'SS':
                    #     print(parsed_data)
                    elif parsed_data['header'] == 'OL':
                        print(parsed_data)
                        f_ol = open(file_portof_ol, 'a+')
                        f_ol.write(str(parsed_data) + '\n')
                        f_ol.close()
                    elif parsed_data['header'] == 'DL':
                        print(parsed_data)
                        f_dl = open(file_portof_dl, 'a+')
                        f_dl.write(str(parsed_data) + '\n')
                        f_dl.close()
                    elif parsed_data['header'] == 'DBS':
                        print(parsed_data['sec'], parsed_data['tradetime'])
                        f_dbs.write(str(parsed_data) + '\n')
                    else:
                        print(parsed_data['header'])
                        # f_else(str(parsed_data) + '\n')
                except Exception as e:
                    PrintException()
                    print('2', e)
    except Exception as e:

        PrintException()
        print('3', e)
        # continue
