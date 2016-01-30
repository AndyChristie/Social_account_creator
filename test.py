from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Driver():

    proxy = ['213.136.79.124:80']

    def get_proxied_driver(self):
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

    def click_elem(self, elem_type, elem):
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.elem_type, elem)))
        
        if elem_type == CLASS_NAME:
            find = find_element_by_class_name
        elem = driver.find(elem).click()

driver = Driver()
driver = driver.get_proxies_n_driver()
driver.get("https://twitter.com/signup")
driver.click_elem(CLASS_NAME, "submit_button")

