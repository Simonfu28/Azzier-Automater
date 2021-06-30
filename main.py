import re
import sys

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import PyQt5
from PyQt5 import QtWidgets, uic, QtGui, QtCore

from configparser import ConfigParser

config = ConfigParser()
config.read('config.cfg')

global driver


class Main(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Main, self).__init__()   # call inherited class
        uic.loadUi('main.ui', self)    # Loads .ui file

        buttonBox = QtWidgets.QDialogButtonBox(self)
        buttonBox.accepted.connect(self.accept)

        self.input = self.findChild(QtWidgets.QLineEdit, 'pmNum')

        self.show()

    def accept(self):
        s = self.input.text()
        t = input_to_list(s)
        print(t)


def input_to_list(input):
    if '-' in input:
        t = re.split(r'-', input)
        t = [int(i) for i in t]
        num_range = range(t[0], t[1] + 1)
        s = list(num_range)
    else:
        s = re.split(r',|, ', input)
    return s


def login(username, password):
    global driver
    # opens webpage
    driver = selenium.webdriver.Chrome(config.get("Azzier", 'chrome_webdriver'))
    driver.get(config.get("Azzier", "pm_URL"))

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
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    app.exec_()


if __name__ == '__main__':
    main()