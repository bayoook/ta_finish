import requests
import json

from datetime import date, datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from threading import Thread
import sseclient
from pprint import pprint
import time



class ta_mantap():
    def __init__(self):
        self.today = date.today()
        day = f"{date.today().day:02d}"
        month = f"{date.today().month:02d}"
        year = f"{date.today().year:02d}"
        fHead = "data/live/live_trade_"
        f_head_2 = "data/order_book/order_book_"
        f_head_3 = "data/portofolio/portofolio_"
        f_head_4 = "data/else/else_"
        f_head_5 = "data/err/err_"
        fFoot = ".txt"
        self.fName = fHead + day + month + year + fFoot
        self.fName2 = f_head_2 + day + month + year + fFoot
        self.fName3 = f_head_3 + day + month + year + fFoot
        self.fName4 = f_head_4 + day + month + year + fFoot
        self.fName5 = f_head_5 + day + month + year + fFoot
        self.ka = 0
        self.url_first = "http://ipotultima.com"
        self.url = ".ipotindonesia.com/ipot/tablet/ulogin.jsp"
        self.url_main = ".ipotindonesia.com/ipot/tablet/screen_ipad_new.jsp"
        self.url_portofolio = ".ipotindonesia.com/ipot/tablet/screen_ipad_new.jsp?p=porto_x"
        self.url_gateway = ".ipotindonesia.com/ipot/tablet/gateway.jsp"
        self.url_requests = ".ipotindonesia.com/ipot/tablet/request.jsp"
        self.url_req = ".ipotindonesia.com/ipot/tablet/request.jsp"
        self.url_pin = ".ipotindonesia.com/ipot/tablet/plogin.jsp"
        self.https = "https://"
        self.url_ = ""
        self.current_url = ""
        self.total = 0
        self.Accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8," \
                      "application/signed-exchange;v=b3"
        self.Accept_Encoding = "gzip, deflate, br"
        self.a_l = "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7"
        self.con = "keep-alive"
        self.u_a = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) " \
                   "Chrome/76.0.3809.100 Safari/537.36"
        self.COOKIE = ""
        self.try_login = 0
        self.try_request = 0
        # self.all_data = [
        #     'GZCO', 'TINS', 'BSDE', 'BBTN', 'SMGR', 'WIKA', 'RICY', 'GIAA', 'BDMN', 'SGRO', 'ELSA', 'MYRX',
        #     'IMAS', 'POLY', 'BRPT', 'SMMA', 'MYOR', 'AALI', 'SMCB', 'RALS', 'UNSP', 'ASII', 'JSMR', 'ROTI',
        #     'BBKP', 'SIMP', 'ANTM', 'EXCL', 'ISAT', 'HEXA', 'NIKL', 'TBLA', 'KAEF', 'BMTR', 'MNCN', 'ITMG',
        #     'SPMA', 'INCO', 'LPKR', 'BMRI', 'LPLI', 'PNLF', 'KLBF', 'BKSL', 'MEDC', 'SCMA', 'SMRA', 'AKRA',
        #     'MASA', 'DOID', 'TKIM', 'BUMI', 'PTPP', 'KKGI', 'MAPI', 'PNBN', 'BWPT', 'INTA', 'PTBA', 'INTP',
        #     'TBIG', 'BBCA', 'RMBA', 'PWON', 'GGRM', 'BHIT', 'BIPI', 'ADMG', 'UNTR', 'LPCK', 'SMSM', 'SMAR',
        #     'BRMS', 'CPIN', 'SSIA', 'ASGR', 'LSIP', 'UNVR', 'TRAM', 'TMPI', 'ICBP', 'KIJA', 'AISA', 'ASRI',
        #     'PGAS', 'AUTO', 'BBRI', 'ADRO', 'BJBR', 'ERAA', 'CTRA', 'BBNI', 'BORN', 'CTRS', 'CMNP', 'KRAS',
        #     'BTPN', 'MAIN', 'JPFA', 'TLKM', 'INVS', 'IATA', 'APLN', 'MDLN', 'BTEL', 'ENRG', 'BISI', 'LCGP',
        #     'DILD', 'ELTY', 'ADHI', 'BRAU', 'INKP', 'GJTL', 'INDS', 'INDR', 'HRUM', 'INDY', 'PTRO', 'INDF'
        # ]
        self.all_data = [
            'TLKM', 'TBIG'
        ]
        self.headers = {}
        self.f_lt = open(self.fName, "a+")
        self.f_ob = open(self.fName2, "a+")
        self.f_portofolio = open(self.fName3, "a+")
        self.f_else = open(self.fName4, "a+")
        self.f_err = open(self.fName5, "a+")

    def start(self):
        print("data save in", self.fName)
        self.open_browser()

    def open_browser(self):
        print("opening browser..")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument(
            '--no-sandbox')  # required when running as root user. otherwise you would get no sandbox errors.
        self.driver = webdriver.Chrome(executable_path='/root/ta/chromedriver',
                                    options=chrome_options,
                                    service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
        self.driver.implicitly_wait(5)
        print("success open browser")
        
        self.find_name()

    def find_name(self):
        try:
            print('opening.. ' + self.url_first)
            self.driver.get(self.url_first)
            url = self.driver.current_url
            url = url.split("/")[2]
            self.current_url = url.split(".")[0]
            self.url_ = self.https + self.current_url
        except:
            self.url_ = self.https + "app14"
        print("")
        self.login()

    def login(self):
        print('opening.. ' + self.url_ + self.url)
        try:
            self.driver.get(self.url_ + self.url)
            print("trying to login..")
            self.driver.find_element_by_id('uid').send_keys('username')
            self.driver.find_element_by_id('pwd').send_keys('password')
            self.driver.find_element_by_id('pwd').send_keys(Keys.RETURN)
        except:
            print("failed to login, trying to relogin..\n")
            return 0
        # print("login success\n")
        self.get_cookies()

    def get_cookies(self):
        print('opening.. ' + self.url_ + self.url_main)
        # self.driver.get(self.url_ + self.url_main)
        # self.driver.find_element_by_class_name('full')
        print("get cookies..")
        all_cookies = self.driver.get_cookies()
        print(self.driver.current_url)
        self.driver.execute_script('submitNewFeature();')
        self.driver.execute_script("loadPopup('popupPIN');")
        self.driver.quit()
        all_cookies_encode = {}

        for cookie in all_cookies:
            all_cookies_encode[cookie['name']] = cookie['value']

        cookieSS_0 = all_cookies_encode['cookieSS_0']
        cookieSS_1 = all_cookies_encode['cookieSS_1']
        cookieSS_2 = all_cookies_encode['cookieSS_2']
        cookieSS_3 = all_cookies_encode['cookieSS_3']
        cookieSS_4 = all_cookies_encode['cookieSS_4']
        cookieSS_5 = all_cookies_encode['cookieSS_5']
        cookieSS_6 = all_cookies_encode['cookieSS_6']
        cookieSS_7 = all_cookies_encode['cookieSS_7']
        cookieSS_8 = all_cookies_encode['cookieSS_8']
        cookieSS_9 = all_cookies_encode['cookieSS_9']
        cookieSS_10 = all_cookies_encode['cookieSS_10']
        cookieSS_11 = all_cookies_encode['cookieSS_11']
        cookieSS_12 = all_cookies_encode['cookieSS_12']
        cookieSS_13 = all_cookies_encode['cookieSS_13']
        cookieOB_0 = all_cookies_encode['cookieOB_0']
        cookieOB_1 = all_cookies_encode['cookieOB_1']
        cookieOB_2 = all_cookies_encode['cookieOB_2']
        JSESSIONID = all_cookies_encode['JSESSIONID']
        self.COOKIE = "JSESSIONID=" + JSESSIONID + "; pickdevice=tablet; vscodeNewFt=5.5.0.5; cookieSS_0=" + \
                      cookieSS_0 + "; cookieSS_1=" + cookieSS_1 + "; cookieSS_2=" + cookieSS_2 + "; cookieSS_3=" + \
                      cookieSS_3 + "; cookieSS_4=" + cookieSS_4 + "; cookieSS_5=" + cookieSS_5 + "; cookieSS_6=" + \
                      cookieSS_6 + "; cookieSS_7=" + cookieSS_7 + "; cookieSS_8=" + cookieSS_8 + "; cookieSS_9=" + \
                      cookieSS_9 + "; cookieSS_10=" + cookieSS_10 + "; cookieSS_11=" + cookieSS_11 + "; cookieSS_12=" \
                      + cookieSS_12 + "; cookieSS_13=" + cookieSS_13 + "; cookieOB_0=" + cookieOB_0 + "; cookieOB_1=" \
                      + cookieOB_1 + "; cookieOB_2=" + cookieOB_2 + "; JSESSIONID=" + JSESSIONID
        print("success get cookies")
        print("cookies :", self.COOKIE, "\n")
        self.scrap_data()

    def scrap_data(self):
        print("request stream page..")
        self.headers = {
            'Accept': self.Accept,
            'Accept-Encoding': self.Accept_Encoding,
            'Accept-Language': self.a_l,
            'User-Agent': self.u_a,
            'COOKIE': self.COOKIE
        }
        data_portof = {'p1': '1', 'p2': '1114120', 'p3': '13', 'p4': 'R10000280220'}
        data_req_acc = {'p1': '1', 'p2': '1114117'}
        data_order = {'p1': '1', 'p2': '1114118', 'p3': '13', 'p4': '*'}
        data_done = {'p1': '1', 'p2': '1114119', 'p3': '13', 'p4': '*'}
        data_dont_know_2 = {'p1': '1', 'p2': '1114119', 'p3': '', 'p4': '*'}
        data_lt = {'p1': '1', 'p2': '1114113', 'p3': '', 'p4': ''}
        data_ob = {'p1': '1', 'p2': '1114115', 'p3': '', 'p4': 'RG', }
        # try:
        sleep(0.1)
        r = self.request_get()
        print("status website :", r.status_code)
        if r.status_code == 500:
            self.try_request += 1
            print("request failed. trying to reconnect..")
        elif r.status_code == 200:
            print(date)
            print("request success.\n")
            self.total = 0
            print("scrap data..\n")
            # Thread(target=self.request_post, args=(data_done,)).start()
            # Thread(target=self.request_post, args=(data_order,)).start()
            # Thread(target=self.request_post, args=(data_portof,)).start()
            # Thread(target=self.request_post, args=(data_dont_know_2,)).start()
            Thread(target=self.request_post, args=(data_lt,)).start()
            # Thread(target=self.request_post, args=(data_req_acc,)).start()
            for x in self.all_data:
                data_ob['p3'] = str(x)
                Thread(target=self.request_post, args=(data_ob,)).start()
            i = 0
            while i < 100:
                try:
                    start_time = time.time()
                    r = self.request_get()
                    client = sseclient.SSEClient(r)
                    # session.post(url + 'request.jsp', data=lt_data)
                    print("%s" % (time.time() - start_time))
                    i += 1
                except Exception as e:
                    print(e)
                    pass
            exit(1)
            client = sseclient.SSEClient(r)
            for event in client.events():
                if self.today != date.today():
                    return 0
                if datetime.now().hour == 8 and datetime.now().minute == 54:
                    return 0
                if event.data == "TIMEOUT":
                    print("TIMEOUT\nPLEASE WAIT TO RECONNECT")
                    event.data = "KEEP-ALIVE"
                    self.start()
                if event.data == 'KEEP-ALIVE':
                    print('KA')
                try:
                    parsed_data = json.loads(event.data)
                    # print(str(datetime.now().hour) + ":" + str(datetime.now().minute), parsed_data[:40])
                    if parsed_data['header'] == 'LT':
                        self.f_lt.write(str(parsed_data) + '\n')
                    elif parsed_data['header'] == 'OB':
                        self.f_ob.write(str(parsed_data) + '\n')
                    elif parsed_data['header'] == 'PC' \
                            or parsed_data['header'] == 'PS' \
                            or parsed_data['header'] == 'AL':
                        self.f_portofolio.write(str(parsed_data) + '\n')
                    else:
                        self.f_else.write(str(parsed_data) + '\n')
                except:
                    self.f_err.write(str(event.data) + '\n')

    def login_trade(self):
        self.driver.execute_script('submitNewFeature();')
        self.driver.execute_script("loadPopup('popupPIN');")
        self.driver.find_element_by_id('input')
        pin = 'pin'
        while len(pin) < 6:
            pin = (input("Masukkan pin : "))
            if len(pin) < 6:
                print("Pin minimal 6 digit")
        for x in pin:
            self.driver.execute_script("addText('input'," + x + ");")
            sleep(0.2)
        self.driver.find_element_by_xpath('//*[@id="popupPIN"]/div/table/tbody/tr/td/form/table/tbody/tr['
                                          '6]/td[3]/input[1]').click()
        self.driver.find_element_by_xpath('//*[@id="toppanel"]/div/ul/li[26]')
        self.get_cookies()

    # def buy_order(self):
    #     buy = input('')
    #     value = buy.split(' ')
    #     code = value[0]
    #     val = value[1]
    #     jumlah = value[2]
    #     label = value[3]
    #     self.driver.execute_script("flag_order_stock = false; centerPopup('popupBuy'); loadPopup('popupBuy'); "
    #                                "call_buysell('buy', 11); cek_draw_acc('buy'); totOB=12; ")
    #     self.driver.find_element_by_id('buy_stockcode').send_keys(code)
    #     self.driver.find_element_by_id('buy_stockcode').send_keys(Keys.RETURN)
    #     harga = '-'
    #     while harga == '-':
    #         harga = self.driver.find_element_by_xpath('//*[@id="tblOrderBook_11"]/tbody/tr[1]/th[3]').text
    #     print(harga)
    #     self.driver.find_element_by_id('buy_price').send_keys(val)
    #     self.driver.find_element_by_id('buy_price').send_keys(Keys.RETURN)
    #     self.driver.find_element_by_id('buy_qty').send_keys(jumlah)
    #     self.driver.find_element_by_id('buy_qty').send_keys(Keys.RETURN)
    #     self.driver.find_element_by_id('buy_label').send_keys(label)
    #     sleep(600)
    #     self.driver.find_element_by_xpath(
    #         '//*[@id="popupBuy"]/div/form/div[1]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/input[2]').click()
    #     self.buy_order()

    def request_get(self):
        return requests.get(self.url_ + self.url_gateway,
                            headers=self.headers,
                            stream=True)

    def request_post(self, data, url_req=''):
        if url_req == '':
            requests.post(self.url_ + self.url_requests,
                          headers=self.headers,
                          data=data)
        else:
            requests.post(self.url_ + url_req,
                          headers=self.headers,
                          data=data)

    def __del__(self):
        print('Something Error, Reprogram')
        self.f_err.close()
        self.f_else.close()
        self.f_portofolio.close()
        self.f_ob.close()
        self.f_lt.close()


while 1:
    ta = ta_mantap()
    try:
        ta.start()
    except Exception as e:
        print(e)


