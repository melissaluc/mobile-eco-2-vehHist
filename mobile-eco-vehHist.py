import os
import time
import logging
import shutil
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup

from modules.helper import veh_id_extract

def main(start_id=0,):
    # initialize chrome driver
    # TODO  DeprecationWarning: executable_path has been deprecated, please pass in a Service object
    driver = webdriver.Chrome("chrome")
    driver.implicitly_wait(20)

    url = r"http://cavl-pvme201:8090/MOBILEvhm/Login?ReturnUrl=%2fMOBILEvhm%2fDevicesGroups%2fVHM" 
    driver.get(url)

    # Mobile-Eco-2 Credentials
    username = "inita"
    password = "init"

    # Login
    driver.find_element("id", "UserShortName").send_keys(username)
    driver.find_element("id", "Password").send_keys(password)

    driver.find_element(By.XPATH, "//div[input/@name='loginRequest']/button[1]").click()

    # Navigate NAV for Dashboard | Control Board | Veh & Components | Realtime Cockpit | Config | Fleet History
    URLS = {
            "fleetHistory":r"http://cavl-pvme201:8090/MOBILEvhm/DevicesGroups/FleetHistory",
            "vehHistory":r"http://cavl-pvme201:8090/MOBILEvhm/DevicesGroups/History",
            }

    # Vehicle History
    driver.get(URLS["vehHistory"])



    # Get all vehicle ID
    pg_src = driver.page_source
    soup = BeautifulSoup(pg_src, 'html.parser')
    veh_id_bs_list= soup.find_all(class_="dxeListBoxItem_DevEx dxeLTM")

    # TODO check veh id list
    veh_id_list = []
    for id in veh_id_bs_list:
        veh_id_list.append(id.get_text())

    start_id = start_id
    end_id = len(veh_id_list)+1

    # Extract CSV files
    for id in veh_id_list[start_id:end_id]:
        print(id)
        if len(id) < 2:
            continue
        else:
            try:
                veh_id_extract (id)
            except Exception:
                return id
            


    driver.quit()
    return print("Finished task!")



