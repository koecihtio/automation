import time
import datetime
import pathlib
import shutil
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


# set webdriver as chrome
driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://my.xmtrading.com/jp/member/signals/calendar')
time.sleep(1)
cookie_btn = driver.find_element_by_xpath('//*[@id="cookieModal"]/div/div/div[1]/div[2]/div/div/button')

# download files, create a new directory, and move the files from downloaded directory to the new directory
if cookie_btn.text == '続行する':
    #---- login and set the condition to download files ----#
    cookie_btn.click()
    account = driver.find_element_by_id('login_user')
    account.send_keys('your account number here')
    password = driver.find_element_by_id('login_pass')
    password.send_keys('your password here')
    time.sleep(1)
    login_btn = driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div[1]/div/form/div[3]/div[2]/button')
    login_btn.click()

    # click on the button to move the pop-up window
    driver.find_element_by_xpath('//*[@id="js-riskCloseButton"]/i').click()

    #---- download files ----#
    # set the desired file
    gbp_jpy = driver.find_element_by_xpath('/html/body/div[2]/div/section/div/div[3]/div[2]/div[1]/div[2]/div/div[1]/ul/li[2]/a')
    usd_jpy = driver.find_element_by_xpath('/html/body/div[2]/div/section/div/div[3]/div[2]/div[1]/div[2]/div/div[1]/ul/li[3]/a')
    nikkei_225 = driver.find_element_by_xpath('/html/body/div[2]/div/section/div/div[3]/div[2]/div[1]/div[2]/div/div[2]/ul/li[5]/a')

    # function: scroll the web page to where the element is located, and click the download botton
    def ActionMoveToClick(driver, element):
        actions = ActionChains(driver)
        actions.move_to_element(element)
        actions.perform()
        time.sleep(1)
        element.click()
        time.sleep(1)
    
    for el in [gbp_jpy, usd_jpy, nikkei_225]: ActionMoveToClick(driver, el)

    # move downloaded files from the downloaded folder to the new created folder
    p = pathlib.Path('your downloaded folder path here')
    directories = list(p.iterdir())
    timestamps = list()
    list_d_name = list()

    for d in directories:
        d_name = d.name
        list_d_name.append(d_name)
        d_path = pathlib.Path(d)
        timestamps.append(datetime.datetime.fromtimestamp(d_path.stat().st_ctime))
    
    df = pd.DataFrame([timestamps, list_d_name]).T
    df.columns = ['time', 'filename']
    df = df.sort_values('time', ascending=False)
    downloaded = list(df[:3]['filename'])
    
    today = str(datetime.date.today())
    original_dir = 'folder path in which you want to create the new folder, here' + today + '/'
    p = pathlib.Path(original_dir)
    p.mkdir(exist_ok=True) # make directory named today's date
    
    for d in downloaded:
        before_dir = 'C:/Users/koeci/Downloads/' + d
        after_dir = original_dir + d
        shutil.move(before_dir, after_dir)
    
    print('The operation has been completed successfully.')
    driver.close()

else:
    print('A different situation than expected has occurred. Terminate the operation.')
    driver.close()