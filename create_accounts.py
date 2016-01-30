from sites import *
import xlrd
import random, string
import atexit
from browser import Driver


email_data = "100Gmail.xlsx"

# All the gmail data from the xlsx file
class Gmail(Twitter, Tumblr, Reddit, Digg, Pinterest, Linkedin, Instagram,
 Driver):

    def __init__(self, name, second_name, email,
                 password, recovery_email):
        self.name           = name
        self.second_name    = second_name
        self.email          = email
        self.password       = password
        self.recovery_email = recovery_email
        #self.driver         = self.get_driver()
        


    def gmail_login(self):
        self.driver.get("""https://accounts.google.com/ServiceLogin?service=mail&continue
                      =https://mail.google.com/mail/#identifier""")
        
        time.sleep(5)
        
        email = self.driver.find_element_by_id("Email")
        email.send_keys(self.email)
        self.driver.find_element_by_id("next").click()
        
        time.sleep(5)
        
        password = self.driver.find_element_by_id("Passwd")
        password.send_keys(self.password)
        self.driver.find_element_by_id("signIn").click()
        
        recovery_email = self.driver.find_element_by_id("emailAnswer")
        recovery_email.send_keys(self.recovery_email)
        self.driver.find_element_by_id("submitChallenge").click()
        
        confirm = raw_input("Acivate all accounts then press any key to continue")


#driver = get_driver()

def main(email_data):
    workbook = xlrd.open_workbook(email_data)
    sheet = workbook.sheet_by_index(0)
    
    
    first = 0
    for row in range(sheet.nrows):
        if not first <= 6:
            name           = sheet.cell(row, 0).value # .value return the unicode
            second_name    = sheet.cell(row, 1).value
            email          = sheet.cell(row, 2).value
            password       = sheet.cell(row, 3).value
            recovery_email = sheet.cell(row, 4).value
            
            accounts = Gmail(name=name, second_name=second_name, 
                             email=email, password=password, 
                             recovery_email=recovery_email)
            accounts.twitter_sign_up()
            accounts.tumblr_sign_up()
            #accounts.pinterest_sign_up()# won't click the sign up button: line 174 sites.py
            accounts.linkedin_sign_up()
            #accounts.instagram_sign_up()# needs an app
            
            accounts.gmail_login()
            
            accounts.save_account(Twitter)
            accounts.save_account(Tumblr)
            #accounts.save_account(Pinterest)
            accounts.save_account(Linkedin)
            #accounts.save_account(Instagram)
        first += 1


if __name__=='__main__':
    main(email_data)

