#!/usr/bin/env python


import datetime, time, json, sys
from color import Text
from msg import success_msg, info_msg, error_msg

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# Specify chromedriver binary
driver_path = '.\\chromedriver_win32\\chromedriver.exe'
service = ChromeService(executable_path=driver_path)

# Run headless + options
options = ChromeOptions()
options.add_argument('--headless=new')
max_wait_time = 10



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

        success_msg('Successfully extracted datetime from element')
        return (True, dt)
    
    except Exception as ex:
        error_msg(str(ex))
        return (False, None)



# Get date/time
def get_datetime(driver):
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

    time.sleep(2)

    return extract_datetime(element)



# Update first and last dates for given dataset
def update_metadata(dataset_name='mvco'):
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(f'https://ifcb-data.whoi.edu/timeline?dataset={dataset_name}')

        success, dt = get_datetime(driver)

        if success:
            dt = str(dt)

            # Get current metadata
            with open('metadata.json', 'r') as f:
                metadata = json.load(f)
            
            # Update metadata
            metadata[dataset_name]['last_date'] = dt

            # Write updated metadata
            with open('metadata.json', 'w') as f:
                json.dump(metadata, f)
            
            text = f'Successfully updated metadata for \'{dataset_name}\''
            success_msg(text)

            return (driver, dt)
        
        else:
            raise Exception('extract_datetime() failed')
    
    except Exception as ex:
        error_msg(f'Updating metadata for \'{dataset_name}\' failed')
        error_msg(str(ex))

        driver.quit()



def get_last_date(dataset_name):
    try:
        with open('metadata.json', 'r') as f:
            metadata = json.load(f)
        return (True, metadata[dataset_name]['last_date'])
    except Exception as ex:
        error_msg(f'Getting latest date for \'{dataset_name}\' failed')
        error_msg(str(ex))
        return (False, None)



def get_first_date(dataset_name):
    try:
        with open('metadata.json', 'r') as f:
            metadata = json.load(f)
        return (True, metadata[dataset_name]['first_date'])
    except Exception as ex:
        error_msg(f'Getting latest date for \'{dataset_name}\' failed')
        error_msg(str(ex))
        return (False, None)



def get_data(dataset_name, start_date=None, end_date=None):

    # Update metadata
    driver, current_dt = update_metadata(dataset_name)
    time.sleep(1)

    info_msg(str(current_dt))

    try:

        text = f'UPDATED FINISED for \'{dataset_name}\''
        info_msg(text)

        # Keep going back until end_date found
        if end_date is None:
            success, end_date = get_last_date(dataset_name)
            if not success:
                raise Exception('get_last_date() failed')
        success, end_date = extract_datetime(end_date)
        if not success:
            raise Exception('extract_datetime() failed')
        while current_dt > end_date:
            'D20230620T005203_IFCB127'
    
    except Exception as ex:
        error_msg(f'Getting data for \'{dataset_name}\' failed')
        error_msg(str(ex))
    
    finally:
        driver.quit()




    #IFCB5_2017_008_221501



def main():
    get_data('mvco')
    get_data('SPIROPA')
    #get_data('mvco', '2023-06-15 17:16:36', '2023-06-18 02:13:19')
    #print(get_last_date('mvco'))
    #print(get_first_date('SPIROPA'))

    get_data('mvco', '2023-06-15 17:16:36', '2023-06-18 02:13:19')


if __name__ == '__main__':
    main()
