import requests as req
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

import re


class Student_In_Meeting:
    def __init__(self):
        opt = Options()
        opt.add_argument("--disable-infobars")
        #opt.add_argument("start-maximized")
        opt.add_argument("--disable-extensions")
        # Pass the argument 1 to allow and 2 to block
        opt.add_experimental_option("prefs", { 
            "profile.default_content_setting_values.media_stream_mic": 2, 
            "profile.default_content_setting_values.media_stream_camera": 2,
            "profile.default_content_setting_values.geolocation": 2, 
            "profile.default_content_setting_values.notifications": 2 
        })
        self.driver = webdriver.Chrome(chrome_options=opt)
        self.driver.implicitly_wait(20)

    def go_to_tab(self, handler):
        all_handlers = self.driver.window_handles
        for w in all_handlers:
            if w == handler:
                self.driver.switch_to.window(w)
                return True
        return False

    def new_tab(self, link):
        self.driver.execute_script("window.open('{}');".format(link))
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return self.driver.current_window_handle

    def remove_current_tab(self, previous_handler='NULL'):
        self.driver.execute_script("window.close();")
        self.driver.switch_to.window(
            previous_handler if previous_handler != 'NULL' and previous_handler in self.driver.window_handles else self.driver.window_handles[0])
        return True

    def go_in_meeting(self, url, name, init_msg=[]):
        dict_answer = {'tab_handler': self.new_tab(url), 'url': url, 'name': name, 'status': None}

        input_id = re.findall("<input required=\"required\" class=\"form-control join-form\".+id=\"(.+)\" />",
                              req.get(url).text)[0]
        name_input = self.driver.find_element_by_id(input_id)
        name_input.send_keys(name, Keys.ENTER)
        
        try:
            btn_just_listen = self.driver.find_element_by_xpath("//i[contains(@class, 'icon-bbb-listen')]")
        except NoSuchElementException:
            dict_answer['status'] = False
            return dict_answer
        
        btn_just_listen.click()

        for i, j in init_msg:
            if j:
                self.send_msg(i)

        dict_answer['status'] = True
        return dict_answer

    def send_msg(self, msg):
        self.driver.find_element_by_id("message-input").send_keys(msg, Keys.ENTER)

    def exit_meeting(self, handler):
        current_handler = self.driver.current_window_handle
        if not self.go_to_tab(handler):
            return False
        #self.driver.find_element_by_id("tippy-4").send_keys(Keys.ENTER)
        self.driver.find_element_by_xpath("//i[contains(@class, 'icon-bbb-more')]").send_keys(Keys.ENTER)
        self.driver.find_element_by_xpath("//i[contains(@class, 'icon-bbb-logout')]").send_keys(Keys.ENTER)
        self.remove_current_tab(current_handler)
        return True

    def browse_quit(self):
        self.browse_quit()
        self.driver.quit()

    def check_exists_by_xpath(self, xpath):
        return len(self.driver.find_elements_by_xpath(xpath)) > 0

    def is_ended(self):
        return self.check_exists_by_xpath("//i[contains(@class, 'icon-bbb-logout')]")
