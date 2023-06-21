#!/usr/bin/env python


import datetime, time, json, platform
from msg import start_msg, success_msg, info_msg, error_msg, attention_msg, end_msg

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# Specify chromedriver binary
driver_path = './chromedriver_linux64/chromedriver'
if platform.system() == 'Windows':
    driver_path = '.\\chromedriver_win32\\chromedriver.exe'
service = ChromeService(executable_path=driver_path)

# Run headless + options
options = ChromeOptions()
#options.add_argument('--headless=new')
max_wait_time = 30



# Extract date + time
def extract_datetime(date):
    try:
        # If element is a string
        if isinstance(date, str):
            date_time_arr = date.split()
            date_str = date_time_arr[0]
            time_str = date_time_arr[1]

        # If element is type of WebElement
        else:
            inner_html = date.get_attribute('innerHTML').split('<br>')
            date_str = inner_html[0]
            time_str = inner_html[1].split()[0]

        date_arr = date_str.split('-')
        year = int(date_arr[0])
        month = int(date_arr[1])
        day = int(date_arr[2])

        time_arr = time_str.split(':')
        hour = int(time_arr[0])
        minute = int(time_arr[1])
        second = int(time_arr[2])

        dt = datetime.datetime(year, month, day, hour, minute, second)

        success_msg('extract_datetime() SUCCESS: Successfully extracted datetime from element')
        return dt

    except Exception as ex:
        raise Exception('extract_datetime() FAIL -> ' + str(ex))



# Get date/time
def get_datetime(driver):
    try:
        # Explicit waiting strategy
        wait = WebDriverWait(driver, max_wait_time)

        # Wait until 'Date/Time' element + inner text found
        element_locator = (By.ID, 'stat-date-time')
        element = wait.until(EC.presence_of_element_located(
            element_locator
        ))
        info_msg('found \'stat-date-time\' element')

        wait.until(EC.text_to_be_present_in_element(
            element_locator, '20'
        ))
        info_msg('found inner html for \'stat-date-time\'')

        time.sleep(0.1)

        extracted_dt = extract_datetime(element)
        success_msg('get_datetime() SUCCESS: Successfully extracted datetime from page')
        return extracted_dt
    
    except Exception as ex:
        raise Exception('get_datetime() FAIL -> ' + str(ex))



# Update first and last dates for given dataset
def update_metadata(driver, dataset_name='mvco'):

    try:
        driver.get(
            f'https://ifcb-data.whoi.edu/timeline?dataset={dataset_name}')

        dt = get_datetime(driver)

        # Get current metadata
        with open('metadata.json', 'r') as f:
            metadata = json.load(f)

        # Update metadata
        metadata[dataset_name]['last_date'] = str(dt)

        # Write updated metadata
        with open('metadata.json', 'w') as f:
            json.dump(metadata, f)

        success_msg(f'update_metadata() SUCCESS: Successfully updated metadata for \'{dataset_name}\'')
        return dt

    except Exception as ex:
        raise Exception('update_metadata() FAIL -> ' + str(ex))



def get_last_date(dataset_name):
    try:
        with open('metadata.json', 'r') as f:
            metadata = json.load(f)
        success_msg(f'get_last_date() SUCCESS: Successfully read last date for \'{dataset_name}\'')
        return metadata[dataset_name]['last_date']
    except Exception as ex:
        raise Exception('get_last_date() FAIL -> ' + str(ex))



def get_first_date(dataset_name):
    try:
        with open('metadata.json', 'r') as f:
            metadata = json.load(f)
        success_msg(f'get_first_date() SUCCESS: Successfully read first date for \'{dataset_name}\'')
        return metadata[dataset_name]['first_date']
    except Exception as ex:
        raise Exception('get_first_date() FAIL -> ' + str(ex))



def click_prev_bin(driver, current_url):
    try:
        info_msg('Going to previous bin...')

        # Explicit waiting strategy
        wait = WebDriverWait(driver, max_wait_time)

        # Wait for 'Previous Bin' element to be clickable
        # aka when 'stat-date-time' element has visible text
        element_locator = (By.ID, 'stat-date-time')
        element = wait.until(EC.presence_of_element_located(
            element_locator
        ))
        info_msg('1) found \'stat-date-time\' element')
        wait.until(EC.text_to_be_present_in_element(
            element_locator, '20'
        ))
        info_msg('2) found inner html for \'stat-date-time\'')

        # Wait until 'Previous Bin' element found
        element_locator = (By.ID, 'previous-bin')
        element = wait.until(EC.presence_of_element_located(
            element_locator
        ))
        info_msg('3) found \'previous-bin\' element')
        info_msg('4) ready to click \'previous-bin\' element')
        
        element.click()

        # Wait for new page to fully load
        while driver.current_url == current_url:
            info_msg('waiting for previous page to load...')
            time.sleep(0.1)
        
        success_msg('click_prev_bin() SUCCESS')
        
    except Exception as ex:
        raise Exception('click_prev_bin() FAIL -> ' + str(ex))



def click_next_bin(driver, current_url):
    try:
        info_msg('Going to next bin...')

        # Explicit waiting strategy
        wait = WebDriverWait(driver, max_wait_time)

        # Wait for 'Next Bin' element to be clickable
        # aka when 'stat-date-time' element has visible text
        element_locator = (By.ID, 'stat-date-time')
        element = wait.until(EC.presence_of_element_located(
            element_locator
        ))
        info_msg('1) found \'stat-date-time\' element')
        wait.until(EC.text_to_be_present_in_element(
            element_locator, '20'
        ))
        info_msg('2) found inner html for \'stat-date-time\'')

        # Wait until 'Next Bin' element found
        element_locator = (By.ID, 'next-bin')
        element = wait.until(EC.presence_of_element_located(
            element_locator
        ))
        info_msg('3) found \'next-bin\' element')
        info_msg('4) ready to click \'next-bin\' element')
        
        element.click()

        # Wait for new page to fully load
        while driver.current_url == current_url:
            info_msg('waiting for next page to load...')
            time.sleep(0.1)
        info_msg('new page done loading...')
        
        success_msg('click_next_bin() SUCCESS')
        
    except Exception as ex:
        raise Exception('click_next_bin() FAIL -> ' + str(ex))



def download_zip(driver):
    try:
        info_msg('Downloading zip for current bin...')

        # Explicit waiting strategy
        wait = WebDriverWait(driver, max_wait_time)

        # Wait for Zip download element to be clickable
        # aka when 'stat-date-time' element has visible text
        element_locator = (By.ID, 'stat-date-time')
        element = wait.until(EC.presence_of_element_located(
            element_locator
        ))
        info_msg('1) found \'stat-date-time\' element')
        wait.until(EC.text_to_be_present_in_element(
            element_locator, '20'
        ))
        info_msg('2) found inner html for \'stat-date-time\'')

        # Wait until Zip download element found
        element_locator = (By.ID, 'download-zip')
        element = wait.until(EC.presence_of_element_located(
            element_locator
        ))
        info_msg('3) found \'download-zip\' element')
        info_msg('4) ready to click \'download-zip\' element')
        
        element.click()
        
        success_msg('download_zip() SUCCESS')
        
    except Exception as ex:
        raise Exception('download_zip() FAIL -> ' + str(ex))



def get_data(dataset_name, start_date=None, end_date=None):
    try:
        start_msg(f'Getting \'{dataset_name}\' data from {start_date} to {end_date}...')
        #driver = webdriver.Chrome(service=service, options=options)
        driver = webdriver.Chrome(options=options)

        # Update metadata
        current_dt = update_metadata(driver, dataset_name)

        time.sleep(1)

        info_msg(str(current_dt))

        info_msg(f'UPDATED FINISED for \'{dataset_name}\'')

        # Keep going back until end_date found
        if end_date is None:
            end_date = get_last_date(dataset_name)
        end_date = extract_datetime(end_date)
        while current_dt > end_date:
            attention_msg(f'-------------------Current date: {current_dt}-------------------')
            click_prev_bin(driver, driver.current_url)
            current_dt =  get_datetime(driver)

        # Keep download until start_date found
        if start_date is None:
            start_date = get_first_date(dataset_name)
        start_date = extract_datetime(start_date)
        while current_dt >= start_date:
            attention_msg(f'-------------------Current date: {current_dt}-------------------')
            download_zip(driver)
            click_prev_bin(driver, driver.current_url)
            current_dt = get_datetime(driver)

        # Click one more time
        click_prev_bin(driver, driver.current_url)

        time.sleep(5)
        start_msg(f'Done getting data from \'{dataset_name}\'!')
    except Exception as ex:
        error_msg('get_data() FAIL -> ' + str(ex))

    finally:
        driver.quit()



def main():
    #get_data('mvco')
    #get_data('SPIROPA')
    # get_data('mvco', '2023-06-15 17:16:36', '2023-06-18 02:13:19')
    # print(get_last_date('mvco'))
    # print(get_first_date('SPIROPA'))

    get_data('mvco', '2023-06-21 10:17:04', '2023-06-21 14:19:30')


if __name__ == '__main__':
    main()
