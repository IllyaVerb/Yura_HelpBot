import requests as req
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import re

class Student_In_Meeting:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(60)


    def go_in_meeting(self, url, name, init_msg=[]):
        self.driver.get(url)

        input_id = re.findall("<input required=\"required\" class=\"form-control join-form\".+id=\"(.+)\" />",
                              req.get(url).text)[0]
        name_input = self.driver.find_element_by_id(input_id)
        name_input.send_keys(name, Keys.ENTER)

        
        try:
            btn_just_listen = self.driver.find_element_by_xpath("//button[@aria-label='Только слушать']")
        except NoSuchElementException:
            return False
        btn_just_listen.click()

        for i, j in init_msg:
            if j:
                self.send_msg(self, i)
                #self.driver.find_element_by_id("message-input").send_keys(i, Keys.ENTER)

        #while (True):
        #    txt = input("Your msg: ")
        #    if txt == "ESC":
        #        break
        #    print("Send:", txt)
        #    self.driver.find_element_by_id("message-input").send_keys(txt, Keys.ENTER)

        return True


    def send_msg(self, msg):
        self.driver.find_element_by_id("message-input").send_keys(msg, Keys.ENTER)


    def exit_meeting(self):
        self.driver.find_element_by_id("tippy-4").send_keys(Keys.ENTER)
        self.driver.find_element_by_xpath("//li[@aria-labelledby='dropdown-item-label-15']").send_keys(Keys.ENTER)
        self.driver.find_element_by_xpath("//button[@description='Выйти из конференции']").send_keys(Keys.ENTER)
        browse_quit()


    def browse_quit(self):
        self.driver.quit()


    def check_exists_by_xpath(xpath):
        return len(webdriver.find_elements_by_xpath(xpath)) > 0


    def is_ended(self):
        return check_exists_by_xpath("//button[@description='Выйти из конференции']")
