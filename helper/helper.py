#  Helper functions
import os
import time
import logging
import shutil
import re
import pandas as pd

import glob
from datetime import date

def text_from_html(body):
    """
    This function looks for 'No data to display'
    to skip downloading the CSV

    """

    print("text_from_html called")
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll("div",text=re.compile('No data to display'))
    try:
        return print(u" ".join(t.strip() for t in texts))
    except Exception as e:
        return 0


def veh_id_extract (veh_id):
    """
    Input veh_id one vehicle at a time
    Date Range (start_date,end_date)
    """
    #  Pass vehicle id to ID input
    try:
        veh_id_input_element = driver.find_element(By.XPATH,"//input[@id='comboBoxVehicleSearch_I']")
        veh_id_input_element.clear()
        veh_id_input_element.send_keys(veh_id)
        
    except Exception as e:
        logging.info(f"{veh_id} could not be found in drop down/n {e}")
    
    #  Navigate to APPLY
    # wait for drop down list to load
    wait = WebDriverWait(driver, 30)
    time.sleep(10)

    driver.find_element(By.XPATH,"//btn[@onclick='historyFilter_Submit()']").click()

    # if text_from_html(driver.page_source) != 0:
    #     return

    # Wait for tables to load and export button to load
    time.sleep(30)

    # Navigate to EXPORT button
    try:
        wait.until(EC.presence_of_all_elements_located((By.XPATH,"//button[@type='button' and @aria-haspopup='true']")))

        export_button = driver.find_element(By.XPATH,"//button[contains(text(),'Export')]").click()
        export_csv = driver.find_element(By.XPATH,'//*[@id="historyParentCallback"]/div/div/div[4]/div/div/button[3]').click()
    except Exception as e:
        logging.info(f"Export button not clickable/n {e}")
        return print("Error - Ending routine")


    # Download buffer time
    time.sleep(20)
    logging.info("Downloading CSV file")

    # Rename CSV file and move to OUTPUT folder
    origin = r'C:\Users\MelissaLu\Downloads'
    target = r'C:\Users\MelissaLu\OneDrive - Metrolinx\Desktop\Projects\Mobile Eco-2 Scraping\output'

    downloaded_fn = "historyMasterGrid.csv"

    my_file = os.path.join(origin,downloaded_fn)

    target_loc = os.path.join(target,downloaded_fn)
    


    shutil.move(my_file, target_loc)

    os.chdir(target)

    os.rename("historyMasterGrid.csv" , f"historyMasterGrid_{veh_id}.csv")
    logging.info(f"Downloading historyMasterGrid_{veh_id}.csv is complete")

    time.sleep(30)

    return print(f'File downloaded for {veh_id}')

# if df empty then do not append

def csv_dataset ():


    # use glob to get all the csv files 
    # in the folder
    # path = os.getcwd()

    path = r"C:\Users\MelissaLu\OneDrive - Metrolinx\Desktop\Projects\Mobile Eco-2 Scraping\output"
    csv_files = glob.glob(os.path.join(path, "*.csv"))

    sub_str1 = "_"
    sub_str2 = ".csv"

    df_list = []
    # loop over the list of csv files
    for f in csv_files:
        
        # read the csv file
        df = pd.read_csv(f)
        if df.empty == True:
            continue

        s=str(re.escape(sub_str1))
        e=str(re.escape(sub_str2))
        res=re.findall(s+"(.*)"+e,f)[0]

        df.insert(0,"veh_ID",res)

        df_list.append(df)
        

    df_eco2 = pd.concat(df_list)

    output_filename = f"historyMasterGrid_{date.today()}.csv"
    target = r"C:\Users\MelissaLu\OneDrive - Metrolinx\Desktop\Projects\Mobile Eco-2 Scraping"
    
    df_eco2.to_csv(os.path.join(target,output_filename))