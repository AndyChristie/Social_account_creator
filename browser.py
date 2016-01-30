from selenium import webdriver
from selenium.webdriver.common.proxy import *
import urllib


class Driver:
    proxies = []

    @staticmethod
    def test_proxy(proxy):
        try:
            urllib.urlopen(
                "https://www.google.com",
                proxies={'http': proxy})
            return True
        except IOError:
            print "Connection error! (Check proxy)"
            return False
        else:
            return False

    def get_driver(self):
        for proxy in self.proxies:
            try:
                myproxy = self.proxies.pop()
                if self.test_proxy(myproxy):
                    proxy = Proxy({
                                'proxyType': ProxyType.MANUAL,
                                'httpProxy': myproxy,
                                'ftpProxy': myproxy,
                                'sslProxy': myproxy,
                                'noProxy': '' # set this value as desired
                                  })
                    driver     = webdriver.Firefox(proxy=proxy)###### chrome, phantom js & IE etc ##
                    driver.get("https://www.google.com")
                    is_working = raw_input('Is your proxy working? [y/n]: ') # use selenium assert
                    if is_working == 'y' or is_working == 'Y':
                        return driver
                    if is_working == 'n' or is_working == 'N':
                        driver.quit()
                        continue
                    if not is_working == 'y' or is_working == 'Y' or is_working == 'n' or is_working == 'N':
                        print 'Invallid'
            except:
                continue

    # needs working_proxies.txt in the same dir
    def get_proxies(self):
        with open('working_proxies.txt', 'rb') as working_proxies:
            for proxy in working_proxies:
                proxy.rstrip()
                self.proxies.append(proxy.decode('ascii'))

    def get_driver1(self):
        self.get_proxies()
        driver = self.get_driver()
        return driver

#driver = Driver()
#driver = driver.get_driver()
#driver.get("https://www.youtube.com/watch?v=BmPFioq1l6o&index=102&list=PLihUZHHwjm2GtO_ikMyDg7ot1ENmmYodL")
