import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import PyQt5
from PyQt5 import QtWidgets, uic, QtGui

from configparser import ConfigParser

config = ConfigParser()
config.read('config.cfg')

# opens webpage
driver = selenium.webdriver.Chrome(config.get("Azzier", 'chrome_webdriver'))
driver.get(config.get("Azzier", "pm_URL"))


def login(username, password):
    # closes timeout popup
    timeout_obj = driver.switch_to.alert
    timeout_obj.accept()

    username_box = driver.find_element_by_id('tbxUserId')
    password_box = driver.find_element_by_id('tbxPassword')
    login_button = driver.find_element_by_id('btnLogon')

    username_box.send_keys(username)
    password_box.send_keys(password)
    login_button.click()


def search_pm(pmnum):
    driver.implicitly_wait(5)
    driver.switch_to.frame('mainmodule')
    pm_num = driver.find_element_by_id('txtpmnum')
    pm_num.send_keys(pmnum)
    pm_num.send_keys(Keys.ENTER)


def change_WOgeneration(bool):
    WOgeneration = driver.find_element_by_id()


def main():
    login(config.get("Azzier", 'username'), config.get('Azzier', 'password'))
    search_pm('512')


if __name__ == '__main__':
    main()