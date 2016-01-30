from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.orm import sessionmaker
from models import *
import atexit
import time
import string
import random

#cook = session.query(Twitter.cookies).filter(Twitter.id==self.id).all()
# follow, like and add etc from this file create accounts in an another file
# TODO: Generate content
# TODO: Generate random usernames


class Accounts:
    Session = sessionmaker(bind=engine)
    session = Session()

    def __init__(self, driver):
        self.driver  = driver

#   Gets the account from the db using the accounts id
    def login(self):
        cook = self.session.query(self.table.cookies).filter(self.table.id==self.id).all()
        self.driver.get(self.url)
        for c in cook:
            for cookies in c:
                for cookie in cookies:
                    del cookie['domain'] # uncomment this if you get different domain error
                    self.driver.add_cookie(cookie)
        self.driver.get(self.url) # Reload & you will be logged in automatically
        return self.driver

    def save_account(self, table):
        account = table(id=self.id, email=self.email, password=self.password,
                        cookies=self.cookies, limit_reached=False)
        self.session.add(account)
        self.session.commit()

    def search(self, search_term):
        url = self.search_url %(search_term)
        self.driver.get(url)
        return self.driver

    def get_count(self):
        return self.session.query(self.table.word_list_count).filter(self.table.id==self.id).all()

    def update_count(self, new_count):
        update = self.table(word_list_count=new_count)
        self.session.add(update)
        self.session.commit()

    def generate_password(self, length): # Can't have the same passwords as the gmails or any other
        return ''.join(random.choice(string.lowercase) for i in range(length))

    def generate_username(self):
        ran = ''.join(random.choice(string.lowercase) for i in range(3))
        username = str(self.name) + str(self.second_name) + str(ran)
        return username

    def browser(self, sign_up_url, count): # set count to 0 to add proxies or 1 to leave proxies
        count = 0
        if count == 0:
            driver = self.get_driver1()
        elif not count == 0:
            driver = self.get_driver()
        for i in range(0, 7):
            try:
                driver.get(sign_up_url)
                return driver
            except:
                print "site is refusing proxies"
            count + 1

    def create_id(self):
        cook = self.session.query(self.table.accounts).filter(self.table.sites==self.sites).all()
        cook += 1
        return cook


#-----------------------------------------------------------------------

class Twitter(Accounts):
    url        = "https://twitter.com"
    search_url = "https://twitter.com/search?f=users&vertical=news&q=%s&src=typd"
    table = Twitter

    def click_follow_buttons(self):
        current_count = 0
        while current_count <= 6:
            follow_buttons = self.driver.find_elements_by_class_name("user-actions-follow-button")
            follow_buttons.reverse()
            if len(follow_buttons) >= 1:
                try:
                    for button in range(0,1):
                        if follow_buttons[button].is_displayed():
                            follow_buttons[button].click() # pop didn't work
                            #if driver.find_elements_by_class_name("message-text"):
                            #    return False     # This is for the 1000 follow limit
                            time.sleep(5)
                            pass
                        pass # clicks the follow button at the bottom
                        current_count += 1
                except:
                    pass
            else:
                return False
        try:
            follow_buttons = self.driver.find_elements_by_class_name("user-actions-follow-button")
            for button in range(0,len(follow_buttons)):
                if follow_buttons[button].is_displayed():
                    follow_buttons[button].click() # clicks all the follow buttons on the page 
        except:
            pass

    def run_follow(self, id):
        atexit.register(update_count, count)
        count         = get_count()
        new_word_list = []
        with open('word_list.txt', 'rb') as word_list:
            for word in word_list:
                new_word_list.append(word)
        current_list = new_word_list[first_count:]
        for word in current_list:
            search(driver, word)
            if click_follow_buttons(driver) == False:
                continue
            count += 1

    def twitter_sign_up(self):
        password    = self.generate_password(15)
        sign_up_url = "https://twitter.com/signup"
        name        = self.generate_username()
        fullname    = self.name + ' ' + self.second_name
        #self.driver.get(sign_up_url)
        driver      = self.browser(sign_up_url, 0)
        
        ele = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, "user[name]")))
        driver.find_element_by_name("user[name]").send_keys(fullname) #EC
        #self.driver.find_element_by_name("user[name]").send_keys(fullname) #EC
        driver.find_element_by_name("user[email]").send_keys(self.email)
        driver.find_element_by_name("user[user_password]").send_keys(password)
        driver.find_element_by_id("submit_button").click()
        # new page
        WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, "skip-link")))
        driver.find_element_by_class_name("skip-link").click()
        # new page
        WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, "username")))
        driver.find_element_by_id("username").send_keys(username)
        driver.find_element_by_id("submit_button").click()
        # new page
        WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, "StartCongratulations-buttons")))
        driver.find_element_by_class_name("StartCongratulations-buttons").click()
        # new page
        WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, "StartActions")))
        driver,find_element_by_class_name("StartActions").click()
        # new page /f & c button
        WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, "StartActions")))
        driver.find_element_by_class_name("StartActions").click()
        # new page
        WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, "js-navjs-skip-step")))
        driver.find_element_by_class_name("js-navjs-skip-step").click()
        # new page
        WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, "StartPage-nextu-floatRightjs-navjs-skip-step")))
        driver.find_element_by_class_name("StartPage-nextu-floatRightjs-navjs-skip-step").click()
        # new page
        profile = raw_input('When account is created press any key and Enter to continue: ')
        
        #self.driver.find_element_by_id("submit_button").click() #EC
        
        # "btn u-size4of10 primary-btn StartCongratulations-button js-complete-step js-nav" href="/i/start/select_interests"
        # "StartCongratulations-buttons"
        
        # continue button
        # class "StartActions"
        # class "btn primary-btn"
        
        # follow & continue button
        # class "StartActions"
        # class "btn primary-btn btn-follow-all"
        
        # upload photo page
        # skip button
        # class "js-nav js-skip-step"
        
        # skip button
        # class "StartPage-next u-floatRight js-nav js-skip-step"

#-----------------------------------------------------------------------

class Tumblr(Accounts):
    url = "https://www.tumblr.com/"
    table = Tumblr

    def tumblr_sign_up(self):
        url = "https://www.tumblr.com/"
        password    = self.generate_password(15)
        name        = self.generate_username()
        self.driver.get(sign_up_url)
        
        self.driver.find_element_by_name("tumblelog[name]").send_keys(name)
        self.driver.find_element_by_name("user[email]").send_keys(self.email)
        self.driver.find_element_by_name("user[password]").send_keys(password)
        self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[3]/div[1]/button").click()
        captcha = raw_input('When captcha is completed press any key then Enter to continue: ')

#-----------------------------------------------------------------------

class Reddit(Accounts):
    url   = "https://www.reddit.com/"
    table = Reddit

#   No email required
    def reddit_sign_up(self):
        url         = "https://www.reddit.com/login"
        password    = self.generate_password(15)
        name        = self.generate_username()
        self.driver.get(sign_up_url)
        
        self.driver.find_element_by_name("user").send_keys(name)
        self.driver.find_element_by_name("passwd").send_keys(password)
        self.driver.find_element_by_name("passwd2").send_keys(password)
        self.driver.find_element_by_name("rem").click()
        self.driver.find_element_by_class_name("c-btnc-btn-primaryc-pull-right").click()

#-----------------------------------------------------------------------

class Pinterest(Accounts):
    url = "https://www.pinterest.com/"
    table = Pinterest

    def pinterest_sign_up(self):
        url         = "https://www.pinterest.com/"
        password    = self.generate_password(15)
        name        = self.generate_username()
        full_name   = self.name + self.second_name
        self.driver.get(sign_up_url)

        self.driver.find_element_by_name("email").send_keys(self.email)
        self.driver.find_element_by_name("password").send_keys(password)
        self.driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[1]/div/div/div[2]/div[3]/div[1]/div[3]/div/div[1]/div/div[2]/form/div/ul/div[1]/div[2]/li[2]/div/button").click()
        self.driver.find_element_by_name("full_name").send_keys(full_name)
        self.driver.find_element_by_name("age").send_keys(22)
        self.driver.find_element_by_name("gender").click()
        # self.driver.find_element_by_css_selector("").click()
        time.sleep(50)

#-----------------------------------------------------------------------

class Linkedin(Accounts):
    url = "https://www.linkedin.com/"
    table = Linkedin

    def linkedin_sign_up(self):
        password    = self.generate_password(15)
        sign_up_url = "https://www.linkedin.com/"
        self.driver.get(sign_up_url)
        
        self.driver.find_element_by_name("firstName").send_keys(self.name)
        self.driver.find_element_by_name("lastName").send_keys(self.second_name)
        self.driver.find_element_by_name("emailAddress").send_keys(self.email)
        self.driver.find_element_by_name("password").send_keys(password)
        self.driver.find_element_by_class_name("fill-v2").click()
        profile = raw_input('When progile is created press any key and Enter to continue: ')

#-----------------------------------------------------------------------

class Instagram(Accounts):
    url = "https://www.instagram.com/"
    table = Instagram

    def instagram_sign_up(self):
        password    = self.generate_password(15)
        url         = "https://www.instagram.com/"
        full_name   = self.name + ' ' + self.second_name
        name        = self.generate_username() # create method to generate username using first and last name
        self.driver.get(url)
        
        self.driver.find_element_by_xpath("/html/body/span/section/main/article/div[2]/div[1]/div/form/div[2]/input").send_keys(self.email)
        self.driver.find_element_by_name("fullName").send_keys(full_name)
        self.driver.find_element_by_name("username").send_keys(name)
        self.driver.find_element_by_name("password").send_keys(password)
        self.driver.find_element_by_class_name("_1on88_k2yal_84y62_7xso1_nv5lf").click()

#-----------------------------------------------------------------------

class Livejournal(Accounts):
    url = "http://www.livejournal.com/"

    def livejournal_sign_up(self):
        password    = self.generate_password(15)
        sign_up_url = 'https://www.livejournal.com/create'
        self.driver.get(sign_up_url)
        # has a unique captcha
        pass

#-----------------------------------------------------------------------

class Stumbleupon(Accounts):
    url = "http://www.stumbleupon.com/"
# recaptcha

#-----------------------------------------------------------------------

class Digg(Accounts):
    url = "http://digg.com/"
    table = Digg
    # Can only sign up with facebook, twitter and google
    # Use foreign keys

#-----------------------------------------------------------------------


