import json
from datetime import date

import requests
import sseclient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



class ta_mantap():
    def __init__(self):
        day = f"{date.today().day:02d}"
        month = f"{date.today().month:02d}"
        year = f"{date.today().year:02d}"
        fHead = "live_trade_"
        f_head_2 = "all_trade_"
        f_head_3 = "graph_"
        f_head_4 = "oc_"
        fFoot = ".txt"
        self.fName = fHead + day + month + year + fFoot
        self.fName2 = f_head_2 + day + month + year + fFoot
        self.fName3 = f_head_3 + day + month + year + fFoot
        self.fName4 = f_head_4 + day + month + year + fFoot
        self.ka = 0
        self.url_first = "http://ipotultima.com"
        self.url = ".ipotindonesia.com/ipot/tablet/ulogin.jsp"
        self.url_main = ".ipotindonesia.com/ipot/tablet/screen_ipad_new.jsp"
        self.url_gateway = ".ipotindonesia.com/ipot/tablet/gateway.jsp"
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
        self.data = 0
        self.per10 = []

    def start(self):
        self.f = open(self.fName, "a+")
        self.ff = open(self.fName2, "a+")
        self.fff = open(self.fName3, "a+")
        self.ffff = open(self.fName4, "a+")
        print("data save in", self.fName)
        self.open_browser()

    def open_browser(self):
        print("opening browser..")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        # required when running as root user. otherwise you would get no sandbox errors.
        self.driver = webdriver.Chrome(executable_path='/root/ta/chromedriver',
                                       options=chrome_options,
                                       service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
        self.driver.implicitly_wait(10)
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
            self.find_name()
        print("login success\n")
        self.get_cookies()

    def get_cookies(self):
        print('opening.. ' + self.url_ + self.url_main)
        # self.driver.get(self.url_ + self.url_main)
        self.driver.find_element_by_class_name('full')
        print("get cookies..")
        all_cookies = self.driver.get_cookies()
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
        print(self.driver.current_url)
        try:
            r = requests.get(self.url_ + self.url_gateway,
                             headers={'Accept': self.Accept, 'Accept-Encoding': self.Accept_Encoding,
                                      'Accept-Language': self.a_l, 'User-Agent': self.u_a,
                                      'COOKIE': self.COOKIE}, stream=True)
            print("status website :", r.status_code)
            if r.status_code == 500:
                self.try_request += 1
                print("request failed. trying to reconnect..")
                self.find_name()
            elif r.status_code == 200:
                print("request success.\n")
                self.driver.quit()
                client = sseclient.SSEClient(r)
                self.total = 0
                print("scrap data..\n")
                for event in client.events():
                    self.total += 1
                    if event.data == "TIMEOUT":
                        print("TIMEOUT\nPLEASE WAIT TO RECONNECT")
                        event.data = "KEEP-ALIVE"
                        self.start()
                    if event.data == "KEEP-ALIVE":
                        self.ka += 1
                        if self.ka == 10:
                            print(event.data)
                            self.ka = 0
                        else:
                            continue
                    if event.data == "UNKNOWN":
                        continue
                    else:
                        try:
                            parsed_data = json.loads(event.data)
                            if parsed_data['header'] == 'LT':
                                print(event.data)
                                self.f.write(str(event.data))
                                self.f.write('\n')
                                self.fff.write(str(parsed_data['time']))
                                self.fff.write(",")
                                self.fff.write(str(parsed_data['stocks']))
                                self.fff.write(",")
                                self.fff.write(str(parsed_data['price']))
                                self.fff.write('\n')
                            elif parsed_data['header'] == 'OB':
                                print(event.data)
                                self.ff.write(str(event.data))
                                self.ff.write('\n')
                            else:
                                print(event.data)
                                self.ff.write(str(event.data))
                                self.ff.write('\n')
                        except:
                            pass
            self.f.close()
            self.ff.close()
            if self.total == 0:
                self.start()
        except:
            print('failed')
            self.find_name()

    def main(self):
        self.open_browser()
        self.find_name()
        self.login()
        self.get_cookies()
        self.scrap_data()

    def relogin(self):
        self.find_name()
        self.login()


ta = ta_mantap()
ta.start()

