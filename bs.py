import time
from datetime import datetime
import requests
import pickle
import sseclient
import json
import os
import sys
import linecache


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


def request_order(p1, p2, p3, p4, p5, p6, p7, p10):
    session = requests.Session()

    order = {'p1': p1, 'p2': p2, 'p3': p3, 'p4': p4, 'p5': p5, 'p6': p6, 'p7': p7, 'p10': p10}

    with open('session', 'rb') as f:
        cookie = pickle.load(f)

    with open('url', 'r') as f:
        url = f.read()

    with open('header', 'r') as f:
        header = json.loads(f.read().replace("'", '"'))

    a = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Origin': url[:31],
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Referer': url + 'screen_ipad_new.jsp',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
    }

    login_pin = {
        'id_menu': 'qlink',
        'uid': 'username',
        'pin': 'pin'
    }

    session.cookies.update(cookie)
    session.headers.update(header)
    try:
        p_login = session.post(url + 'plogin.jsp', data=login_pin, headers=a)
        print(url)
    except Exception as e:
        print(e)
        pass
    i  = 0
    session.post(url + 'request.jsp', data=order)


def request_amend(p1, p2, p3, p4, p5):
    session = requests.Session()

    order = {'p1': p1, 'p2': p2, 'p3': p3, 'p4': p4, 'p5': p5}
    with open('session', 'rb') as f:
        cookie = pickle.load(f)

    with open('url', 'r') as f:
        url = f.read()

    with open('header', 'r') as f:
        header = json.loads(f.read().replace("'", '"'))

    a = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Origin': url[:31],
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Referer': url + 'screen_ipad_new.jsp',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
    }

    login_pin = {
        'id_menu': 'qlink',
        'uid': 'username',
        'pin': 'pin'
    }

    session.cookies.update(cookie)
    session.headers.update(header)
    try:
        p_login = session.post(url + 'plogin.jsp', data=login_pin, headers=a)
        print(url)
    except Exception as e:
        print(e)
        pass
    i  = 0
    session.post(url + 'request.jsp', data=order)


def request_reject(p1, p2, p3):
    # p1 = 1
    # p2 = 1114124
    # p3 = relid
    session = requests.Session()

    order = {'p1': p1, 'p2': p2, 'p3': p3}
    with open('session', 'rb') as f:
        cookie = pickle.load(f)

    with open('url', 'r') as f:
        url = f.read()

    with open('header', 'r') as f:
        header = json.loads(f.read().replace("'", '"'))

    a = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Origin': url[:31],
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Referer': url + 'screen_ipad_new.jsp',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
    }

    login_pin = {
        'id_menu': 'qlink',
        'uid': 'username',
        'pin': 'pin'
    }

    session.cookies.update(cookie)
    session.headers.update(header)
    try:
        p_login = session.post(url + 'plogin.jsp', data=login_pin, headers=a)
        print(url)
    except Exception as e:
        print(e)
        pass
    i  = 0
    session.post(url + 'request.jsp', data=order)


def status_order():

    session = requests.Session()

    data_order = {'p1': '1', 'p2': '1114118', 'p3': '13', 'p4': '*'}
    data_done = {'p1': '1', 'p2': '1114119', 'p3': '13', 'p4': '*'} 
    data_portof = {'p1': '1', 'p2': '1114120', 'p3': '13', 'p4': 'R10000280220'}
    data_ob = {'p1': '2', 'p2': '5570561', 'p3': ''}
    data_ob2 = {'p1': '1', 'p2': '2228234', 'p3': ''}

    with open('session', 'rb') as f:
        cookie = pickle.load(f)

    with open('url', 'r') as f:
        url = f.read()

    with open('header', 'r') as f:
        header = json.loads(f.read().replace("'", '"'))
    
    a = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Origin': url[:31],
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Referer': url + 'screen_ipad_new.jsp',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,ar-AE;q=0.8,ar;q=0.7',
    }

    login_pin = {
        'id_menu': 'qlink',
        'uid': 'username',
        'pin': 'pin'
    }

    session.cookies.update(cookie)
    session.headers.update(header)

    try:
        p_login = session.post(url + 'plogin.jsp', data=login_pin, headers=a)
    except Exception as e:
        print(e)
        pass
    i  = 0
    x = 'TLKM'
    data_ob['p3'] = x
    data_ob2['p3'] = x
    i += 1
    session.post(url + 'request.jsp', data=data_done)
    session.post(url + 'request.jsp', data=data_order)
    session.post(url + 'request.jsp', data=data_portof)


def jual_beli():
    status_order()
    day = f"{datetime.today().day:02d}"
    month = f"{datetime.today().month:02d}"
    year = f"{datetime.today().year:02d}"

    fFoot = ".txt"
    xxx = day + month + year + fFoot
    while 1:
        try:
            file = open('data/order/order_' + xxx, 'r')
            file_order = open('order_data_' + xxx, 'a+')
            break
        except Exception as e:
            time.sleep(60)
    log_data = open('log_' + xxx, 'w')
    user_label = 'IS'
    code = '1114121'
    cust_code = 'R10000280220'

    while 1:
        saham_list = open('data_saham.txt', 'r').read().splitlines()[1:]
        saham_list = [x.split(' ') for x in saham_list]
        saham_dict = {}
        force_dict = {}
        force_sell = open('force_sell.txt', 'r').read().splitlines()
        force_sell = force_sell[1:] if len(force_sell) > 1 else 0
        # if force_sell:
        #     request_order('1', '1114121', '1', x['sec'], x['price'], '1', 'R10000280220', 'IS')

        for x in saham_list:
            # print(x)
            saham_dict[x[0]] = {
                'lot': int(x[1]),
                'price': int(x[2]),
                'cut_loss': -float(x[3])
            }

        if datetime.now().strftime('%S') != '01':
            status_order()
            time.sleep(2)
            file_ps = open('data/portofolio/ps_' + xxx, 'r')
            data_ps = file_ps.read().replace("'", '"').splitlines()
            data_ps = [json.loads(x) for x in data_ps]
                
            for x in data_ps:
                if x['sec'] in saham_dict:
                    if int(saham_dict[x['sec']]['price']) == 0:
                        saham_dict[x['sec']]['price'] = x['price']
                    if saham_dict[x['sec']]['cut_loss'] >= float(x['pgl']):
                        if int(x['ihand']) > 0 or int(x['unstl']) > 0:
                            request_order('1', '1114121', '1', x['sec'], saham_dict[x['sec']]['price'], x['bal'], 'R10000280220', 'IS')
            # if force_sell:
            #     force_sell = [x.split(' ') for x in force_sell]
                
            # for x in force_sell:
            #     force_dict[x[0]] = {
            #         'price': int(x[1]),
            #     }

            # for x in data_ps:
            #     if x['sec'] in force_dict:
            #         request_order('1', '1114121', '1', x['sec'], force_dict[x['sec']]['price'], x['bal'], 'R10000280220', 'IS')
            
            # open('force_sell.txt', 'w')
                

        # print(saham_dict)
        # exit(1)
        where = file.tell()
        line = file.readline().replace('\'', '"')
        if datetime.now().strftime('%H') == '17':
            return 'done'
        if not line:
            file.seek(where)
            continue
        else:
            try:
                exit(1)
                line = line.replace('\n', '').split(' ')
                nama_saham = line[0]
                if nama_saham in saham_dict:
                    lot = int(saham_dict[nama_saham]['lot'])
                    price_ = int(saham_dict[nama_saham]['price'])
                    cut_loss_ = int(saham_dict[nama_saham]['cut_loss'])
                    # force_ = int(saham_dict[nama_saham][4])
                    time_ = datetime.fromtimestamp(int(line[2][:-2])/1000)
                    x = datetime.now() - time_
                    x = x.total_seconds() / 60
                    print(nama_saham, line[1], time_)
                    log_data.write(nama_saham + str(line[1]) + str(time_) + '\n')
                    open_ = int(line[5])
                    high_ = int(line[6])
                    low_ = int(line[7])
                    close_ = int(line[8])
                    ada_portof = 0
                    ada_order = 0
                    if x >= 5:
                        continue
                    try:
                        os.system('rm data/portofolio/ol_' + xxx)
                        os.system('rm data/portofolio/dl_' + xxx)
                        open('data/portofolio/ol_' + xxx, 'w')
                        open('data/portofolio/dl_' + xxx, 'w')
                    except:
                        print('error')
                        pass
                    status_order()
                    time.sleep(2)
                    file_ps = open('data/portofolio/ps_' + xxx, 'r')
                    data_ps = file_ps.read().replace("'", '"').splitlines()
                    # print(data_ps)
                    ada_portof = 0
                    siap_jual = 0
                    siap_beli = 0
                    ada_order_beli = 0
                    ada_order_jual = 0
                    ada_open_jual = 0
                    ada_open_beli = 0
                    done_beli = 0
                    done_jual = 0
                    ada_saham = 0
                    for x in data_ps:
                        x = json.loads(x)
                        sec = x['sec']
                        if nama_saham == sec:
                            ada_portof = 1

                            if int(x['ihand']) > 0 or int(x['unstl']) > 0:
                                ada_saham = 1

                            # check if ada status done jual / beli
                            if int(x['bdone']) > 0:
                                done_beli = 1
                            if int(x['sdone']) > 0:
                                done_jual = 1

                            # check if ada status open jual / beli
                            if int(x['bopen']) > 0:
                                ada_open_beli = 1
                            if int(x['sopen']) > 0:
                                ada_open_jual = 1

                            # check if ada order jual / beli
                            if int(x['sorder']) > 0:
                                ada_order_jual = 1 
                            if int(x['border']) > 0:
                                ada_order_beli = 1

                    buy_price = low_ if ((high_ - low_) / high_) * 100 < 20 else open_
                    sell_price = high_ if ((high_ - low_) / high_) * 100 < 20 else open_
                    
                    if price_ != 0:
                        buy_price = saham_dict[nama_saham]['price']
                        sell_price = saham_dict[nama_saham]['price']
                    
                    data_ol = open('data/portofolio/ol_' + xxx, 'r').read().splitlines()
                    data_ol = [json.loads(x.replace("'",'"')) for x in data_ol]

                    if len([x for x in data_ol if x['stock'] == nama_saham and x['status'] == 'O']) != 0:
                        stock_ol = [x['stock'] for x in data_ol if x['stock'] == nama_saham and x['status'] == 'O'][-1]
                        
                        price_ol_buy = ([x['prel'] for x in data_ol if x['stock'] == nama_saham and x['status'] == 'O' and x['bs'] == 'B'])
                        price_ol_sell = ([x['prel'] for x in data_ol if x['stock'] == nama_saham and x['status'] == 'O' and x['bs'] == 'S'])
                        price_ol_buy = int(price_ol_buy[-1]) if price_ol_buy else 0
                        price_ol_sell = int(price_ol_sell[-1]) if price_ol_sell else 0
                        id_rel_buy = [x['idrel'] for x in data_ol if x['stock'] == nama_saham and x['status'] == 'O' and x['bs'] == 'B']
                        id_rel_sell = [x['idrel'] for x in data_ol if x['stock'] == nama_saham and x['status'] == 'O' and x['bs'] == 'S']
                        id_rel_buy = id_rel_buy[-1] if id_rel_buy else 0
                        id_rel_sell = id_rel_sell[-1] if id_rel_sell else 0
                        print(stock_ol, price_ol_buy, price_ol_sell, id_rel_buy, id_rel_sell)
                    
                    print(nama_saham, line[1], end=' ')
                    if line[1] == '1': # sell 1 p3
                        if ada_saham or done_beli:
                            # print('sell', nama_saham, ada_portof, siap_jual, siap_beli, ada_order_jual, ada_order_beli, ada_open_jual, ada_open_beli)
                            if ada_open_jual:
                                if not nama_saham in [x['stock'] for x in data_ol]:
                                    print('error on ammend, not stock or cannot read order list')
                                    log_data.write('error on ammend, not stock or cannot read order list\n')

                                if price_ol_sell <= sell_price + (sell_price / 50):
                                    print('amend sell', stock_ol, id_rel_sell, sell_price, price_ol_sell)
                                    log_data.write('amend sell' + str(stock_ol) + str(id_rel_sell) + str(sell_price) + str(price_ol_sell) + '\n')
                                    request_amend('1', '1114122', id_rel_sell, sell_price, lot)
                                    time.sleep(2)
                                else:
                                    print('tidak amend sell', stock_ol, id_rel_sell, buy_price, price_ol_sell)
                                    log_data.write('tidak amend sell' + str(stock_ol) + str(id_rel_sell) + str(sell_price) + str(price_ol_sell) + '\n')
                                
                            elif ada_open_beli:
                                if not nama_saham in [x['stock'] for x in data_ol]:
                                    print('error on reject, not stock or cannot read order list')
                                print('reject buy', stock_ol, id_rel_buy)
                                request_reject('1', '1114124', id_rel_buy)
                                log_data.write('reject buy' + str(stock_ol), str(id_rel_buy) + '\n')
                            elif done_jual:
                                print('tidak jual')
                            else:
                                print('siap jual langsung', sell_price)
                                request_order('1', '1114121', '1', nama_saham, sell_price, '1', 'R10000280220', 'IS')
                                log_data.write('siap jual langsung' + str(sell_price) + '\n')
                        elif done_jual:
                            print('tidak jual')
                            log_data.write('tidak jual\n')
                        elif not ada_saham:
                            print('belum ada saham')
                            log_data.write('belum ada saham\n')
                    elif line[1] == '2': # buy 0 p3
                        if not ada_saham and not done_beli:
                            # print('buy', nama_saham, ada_portof, siap_jual, siap_beli, ada_order_jual, ada_order_beli, ada_open_jual, ada_open_beli)
                            if ada_open_beli:
                                if not nama_saham in [x['stock'] for x in data_ol]:
                                    print('error on ammend, not stock or cannot read order list')
                                    log_data.write('error on ammend, not stock or cannot read order list\n')
                                if price_ol_buy >= buy_price + (buy_price / 50):
                                    print('amend', stock_ol, id_rel_buy, buy_price, price_ol_buy)
                                    log_data.write('amend' + str(stock_ol), str(id_rel_buy), str(buy_price), str(price_ol_buy) + '\n')
                                    request_amend('1', '1114122', id_rel_buy, buy_price, lot)
                                    time.sleep(2)
                                else:
                                    print('tidak amend buy', stock_ol, id_rel_buy, buy_price, price_ol_buy)
                                    log_data.write('tidak amend buy' + str(stock_ol), str(id_rel_buy), str(buy_price), str(price_ol_buy) + '\n')
                                
                            elif ada_open_jual:
                                if not nama_saham in [x['stock'] for x in data_ol]:
                                    print('error on ammend, not stock or cannot read order list')
                                print('reject sell', stock_ol, id_rel_sell)
                                log_data.write('reject sell' + str(stock_ol), str(id_rel_sell) + '\n')
                                request_reject('1', '1114124', id_rel_sell)
                            else:
                                print('siap beli langsung', buy_price)
                                log_data.write('siap beli langsung' + str(buy_price) + '\n')
                                request_order('1', '1114121', '0', nama_saham, buy_price, '1', 'R10000280220', 'IS')
                        # elif done_beli and done_jual:
                        elif done_beli:
                            print('tidak beli')
                            log_data.write('tidak beli\n')
                        elif ada_saham:
                            print('sudah ada saham')
                            log_data.write('sudah ada saham\n')
                    # time.sleep(1)
                    continue
                else:
                    pass
            except Exception as e:
                print('error', e)
                PrintException()
    # time.sleep(1)
start_buy = 'tdone'
try:
    while 1:
        if start_buy == 'tdone':
            start_buy = jual_beli()
            # break
        elif start_buy == 'done':
            try:
                print(datetime.now().strftime('%H%M%S'))
                if datetime.now().strftime('%H') == '09':
                    start_buy = 'tdone'
                    continue
                else:
                    sleep(1)
            except:
                break
except Exception as e:
    print(e)
    PrintException()