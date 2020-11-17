import requests
import pickle
import sseclient
import json
session = requests.Session()  # or an existing session

ob_data = {
    'p1': '1', 
    'p2': '1114114', 
    'p3': 'BBNI', 
    'p4': 'RG',
}

# data_portof = {'p1': '1', 'p2': '1114120', 'p3': '13', 'p4': 'R10000280220'}
# data_req_acc = {'p1': '1', 'p2': '1114117'}
# data_order = {'p1': '1', 'p2': '1114118', 'p3': '13', 'p4': '*'}
# data_done = {'p1': '1', 'p2': '1114119', 'p3': '13', 'p4': '*'}

buy = {'p1': '1', 'p2': '1114121', 'p3': '0', 'p4': 'ENRG', 'p5': '050', 'p6': '1', 'p7': 'R10000280220', 'p10': 'IS'}
# p1 = request asking (1) stop asking (0)
# p2 = special code for buy
# p3 = 0(buy) 1(sell)
# p4 = stock name
# p5 = price
# p6 = qty / lot
# p7 = cust code
# p10 = user label
with open('session', 'rb') as f:
    cookie = pickle.load(f)

with open('url', 'r') as f:
    url = f.read()

with open('header', 'r') as f:
    header = json.loads(f.read().replace("'", '"'))


session.cookies.update(cookie)
session.headers.update(header)

# print(session.cookies)
# print(session.headers)

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
    'pin': 'password'
}
print(a['Origin'])
try:
    p_login = session.post(url + 'plogin.jsp', data=login_pin, headers=a)
    print(url)
except Exception as e:
    print(e)
    pass
i  = 0
import time
# while i < 20:
session.post(url + 'request.jsp', data=data_portof)