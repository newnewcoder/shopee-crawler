import sys
import os
from pathlib import Path
import json
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.ui as ui

class Browser:
    def __init__(self):
        chrome_options = Options()
        
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--window-size=1920,1080')

        if sys.platform == 'linux':
            self.driver = webdriver.Chrome(os.path.abspath('./crawler/driver/linux/chromedriver'), desired_capabilities = chrome_options.to_capabilities())
        elif sys.platform == 'win32':
            self.driver = webdriver.Chrome(os.path.abspath('./crawler/driver/win/chromedriver.exe'), desired_capabilities = chrome_options.to_capabilities())
        elif sys.platform == 'darwin':
            self.driver = webdriver.Chrome(os.path.abspath('./crawler/driver/mac/chromedriver'), desired_capabilities = chrome_options.to_capabilities())

        self.wait = ui.WebDriverWait(self.driver,30)

    def go(self, url):
        self.driver.get(url)
    
    def load_cookie_from(self, cookie_file):
        if(Path(cookie_file).exists()):
            for cookie in pickle.load(open(cookie_file, "rb")):
                #TODO it's a workaround
                if 'SPC_CDS' in json.dumps(cookie):
                    continue
                self.driver.add_cookie(cookie)
            #print('cookie loaded')

    def wait_for(self, method):
        self.wait.until(method)

    def find_by_css(self, path):
        self.wait_for(lambda driver: driver.find_element_by_css_selector(path))
        return self.driver.find_element_by_css_selector(path)

    def find_by_xpath(self, path):
        self.wait_for(lambda driver: driver.find_element_by_xpath(path))
        return self.driver.find_element_by_xpath(path)

    def send_by_css(self, path, *keys):
        el = self.find_by_css(path)
        el.send_keys(*keys)

    def send_by_xpath(self, path, *keys):
        el = self.find_by_xpath(path)
        el.send_keys(*keys)

    def click_by_css(self, path):
        el = self.find_by_css(path)
        el.click()

    def click_by_xpath(self, path):
        el = self.find_by_xpath(path)
        el.click()
    
    def get_cookies(self):
        return self.driver.get_cookies()

    def dump_cookie(self, cookie_file):
        pickle.dump( self.driver.get_cookies() , open(cookie_file,"wb"))
        
    def quit(self):
        self.driver.quit()