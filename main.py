import re
import sys
import time

import selenium
from PyQt5.QtWidgets import QTreeWidgetItem
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys

import PyQt5
from PyQt5 import QtWidgets, uic, QtGui, QtCore

from configparser import ConfigParser

config = ConfigParser()
config.read('config.cfg')

global driver
global pm_list, priority, procedure, workType, dataDivision, generate, inactive


class Main(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Main, self).__init__()  # call inherited class
        uic.loadUi('main.ui', self)  # Loads .ui file

        buttonBox = QtWidgets.QDialogButtonBox(self)
        buttonBox.accepted.connect(self.accept)

        self.input = self.findChild(QtWidgets.QLineEdit, 'pmNum')

        self.generate = self.findChild(QtWidgets.QButtonGroup, 'generate')
        self.generate.buttonClicked.connect(self.unselect)

        self.inactive = self.findChild(QtWidgets.QButtonGroup, 'inactive')
        self.inactive.buttonClicked.connect(self.unselect2)

        self.priority = self.findChild(QtWidgets.QComboBox, 'priority')
        self.procedure = self.findChild(QtWidgets.QComboBox, 'procedure')
        self.workType = self.findChild(QtWidgets.QComboBox, 'workType')
        self.dataDivision = self.findChild(QtWidgets.QComboBox, 'data_division')

        self.changeConfirm = changeConfirm(self)

        self.show()

    def accept(self):
        global pm_list, priority, procedure, workType, dataDivision, generate, inactive
        pm_list = input_to_list(self.input.text())
        priority = self.priority.currentText()
        procedure = self.procedure.currentText()
        workType = self.workType.currentText()
        dataDivision = self.dataDivision.currentText()
        if self.generate.checkedButton() is not None:
            generate = self.generate.checkedButton().text()
        else:
            generate = ''
        if self.inactive.checkedButton() is not None:
            inactive = self.inactive.checkedButton().text()
        else:
            inactive = ''
        self.changeConfirm.show()
        self.changeConfirm.display()

    def unselect(self, radioButton):
        for button in self.generate.buttons():
            if button is not radioButton:
                button.setChecked(False)

    def unselect2(self, radioButton):
        for button in self.inactive.buttons():
            if button is not radioButton:
                button.setChecked(False)


class changeConfirm(QtWidgets.QDialog):
    def __init__(self, parent=Main):
        super(changeConfirm, self).__init__()
        uic.loadUi('change_confirm.ui', self)

        self.changeList = self.findChild(QtWidgets.QListWidget, 'changeList')

        buttonBox = QtWidgets.QDialogButtonBox(self)
        buttonBox.accepted.connect(self.accept)

    def accept(self):
        login(config.get("Azzier", 'username'), config.get("Azzier", 'password'))
        driver.switch_to.frame('mainmodule')
        for i in range(len(pm_list)):
            #print(pm_list[i])
            query()
            search_pm(pm_list[i])
            set_proc(procedure)
            set_workType(workType)
            setActivity(inactive)
            change_WOgeneration(generate)
            save()
        driver.quit()
        self.close()

    def display(self):
        self.changeList.clear()

        pm_string = ', '.join(map(str, pm_list))
        if pm_string != '':
            self.changeList.addItem("These PMs will be changed:\n" + pm_string + "\n")
        if inactive != '':
            self.changeList.addItem("These PMs will be inactivated:\n" + inactive + '\n')
        if priority != '':
            self.changeList.addItem("Priority will be set to:\n" + priority + "\n")
        if procedure != '':
            self.changeList.addItem("Procedure will be changed to:\n" + procedure + '\n')
        if workType != '':
            self.changeList.addItem("Work type will be changed to:\n" + workType + '\n')
        if dataDivision != '':
            self.changeList.addItem("Data division will be changed to:\n" + dataDivision + '\n')
        if generate != '':
            self.changeList.addItem("Work orders will be generated:\n" + generate + '\n')


def input_to_list(pm_input):
    if '-' in pm_input:
        t = re.split(r'-', pm_input)
        z = len(t[0])
        t = [int(i) for i in t]
        num_range = range(t[0], t[1] + 1)
        s = list(num_range)
    else:
        s = re.split(r',|, ', pm_input)
        z = len(s[0])
    s = [str(i).zfill(z) for i in s]
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
    pm_num = driver.find_element_by_id('txtpmnum')
    if pmnum == '':
        pass
    else:
        pm_num.send_keys(pmnum)
        driver.find_element_by_id('txtequipment').click()
        pm_num.send_keys(Keys.ENTER)
    time.sleep(1.5)


def set_proc(proc):
    proc_input = driver.find_element_by_id('txtprocnum')
    craft = driver.find_element_by_id('txtcraft')
    if proc == '':
        pass
    else:
        proc_input.clear()
        craft.clear()
        proc_input.send_keys(proc)
        driver.find_element_by_id('txtequipment').click()


def set_workType(wtype):
    wt_Input = driver.find_element_by_id('txtwotype')
    if wtype == '':
        pass
    else:
        wt_Input.clear()
        wt_Input.send_keys(wtype)


def setActivity(bool):
    inactivate = driver.find_element_by_id('rblinactive_0')
    activate = driver.find_element_by_id('rblinactive_1')
    if bool == 'Yes':
        inactivate.click()
    if bool == 'No':
        activate.click()
    if bool == '':
        pass


def change_WOgeneration(bool):
    WO_ondue = driver.find_element_by_id('rblondue_0')
    WO_oncomplete = driver.find_element_by_id('rblondue_1')
    if bool == 'On Due':
        WO_ondue.click()
    if bool == 'On Complete':
        WO_oncomplete.click()
    if bool == 'All' or '':
        pass


def query():
    driver.implicitly_wait(10)
    query = driver.find_element_by_xpath('/html/body/form/div[3]/div[3]/div/div/div/div/ul/li[1]')
    query.click()


def save():
    save = driver.find_element_by_xpath('/html/body/form/div[3]/div[3]/div/div/div/div/ul/li[5]')
    save.click()
    try:
        driver.switch_to.alert.accept()
    except NoAlertPresentException:
        pass
    time.sleep(1)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    app.exec_()


if __name__ == '__main__':
    main()
