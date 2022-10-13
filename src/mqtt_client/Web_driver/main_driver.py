import os
import selenium
from selenium import webdriver as wb
import time

class WebController(object):

    def __init__(self):
        self.web_driver_path = os.path.join(os.getcwd(), 'Web_driver', 'msedgedriver.exe')
        self.driver = wb.Edge(self.web_driver_path)

    def open_email_and_blackboard(self, e_mail, email_read_time, session_lenght):

        # open email and log in
        if e_mail:
            self.driver.get('https://mail.google.com/mail/u/1/#inbox')
            search_box = self.driver.find_element_by_id('identifierId')
            search_box.send_keys('kuisoko1@sheffield.ac.uk')
            next_buttom = self.driver.find_element_by_id("identifierNext")
            try:
                next_buttom.click()
            except selenium.common.exceptions.ElementClickInterceptedException as err:
                print(err)
                time.sleep(20)
            time.sleep(3)
            username_search_box = self.driver.find_element_by_id('username')
            username_search_box.send_keys('fca19kui')
            password_searchbox = self.driver.find_element_by_id('password')
            password_searchbox.send_keys('keslerisoko20')
            login_button = self.driver.find_element_by_xpath('//*[@id="fm1"]/input[4]')
            login_button.click()
            time.sleep(60*email_read_time)
        else:
            pass

        # blackboard
        self.driver.get('https://vle.shef.ac.uk/?new_loc=%2Fultra%2Fcourse')
        cookiebox = self.driver.find_element_by_id('agree_button')
        cookiebox.click()
        userBox = self.driver.find_element_by_id("user_id")
        userBox.send_keys('fca19kui')
        passwordBox = self.driver.find_element_by_id('password')
        passwordBox.send_keys('keslerisoko20')
        self.driver.find_element_by_id('entry-login').click()
        time.sleep(60*session_lenght)

    def initialize_workflow(self):
        os.system('start "C:/Users/CBE-User 05/OneDrive/Documents/Gymnasium.xlsx"')
        os.system('start https://pomofocus.io')
        os.system('start https://github.com/kesler20/Sofia/blob/master/Context/speaker.py')  # sofia commands

    def get_website(self, url, check_time=None):
        if check_time is None:
            check_time = 150

        driver = self.get_driver(url)
        time.sleep(6)
        push_button = driver.find_element_by_xpath(
            '//*[@id="auth_methods"]/fieldset/div[1]/button'
        )
        push_button.click()
        time.sleep(check_time)
