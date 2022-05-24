from email.mime import base
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from custom_classes import search_bundle
from bs4 import BeautifulSoup
import pandas as pd

def scroll_to_bottom(driver):
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def check_for_popups(driver):

    #if driver.find_element_by_class_name('msg-overlay-list-bubble--is-minimized') is not None:
    found_popup = len(driver.find_elements(By.CLASS_NAME, 'msg-overlay-list-bubble--is-minimized'))
    if found_popup > 0:
        return
    else:
        #if driver.find_element_by_class_name('msg-overlay-list-bubble') is not None:
        #   driver.find_element_by_class_name('msg-overlay-list-bubble').click()
        driver.find_element(By.CLASS_NAME,'msg-overlay-bubble-header__details').find_element(By.CLASS_NAME, "msg-overlay-bubble-header__button").click()
        return

def open_login(driver, username, password):
    #Open login page
    #driver.get(r"https://nanostring.okta.com/app/nanostringtechnologies_bluemountainram_1/exkjp32fejmcV8bME0x7/sso/saml?SAMLRequest=fZExb8IwEIXn%2FgvkPcRxAqQWiURFqyIVFZWIoQsyjoFA4kt9tsTPb5x0oAvezn53997nOYqmbvnC2bP%2BUj9OoR3dmloj7x8y4ozmILBCrkWjkFvJt4v1B2djylsDFiTUZNSdp2XXW2lhK9AZOVvbIg9DLTSgNZU%2BjeFqxVhCE4q2vbu3Sp411HCqFO4PtVMNOG1FpY1o9lGobtdLG7OjujRylx7Wr%2FQ2CxEh9P76xatlRvZlFB3FRKVxmcRHKuUsjaYqZayr0yhmrFe%2BgZGqj5oRa5wa2hGdWmm0QtuMMMpYQCcBS4poylnCKf3uZZu%2FrC%2BVLjvXj8EcBhHy96LYBJvPbUFGO2WwR9MJSD739nm%2F29wBfzxWICrj%2BZLcy0SXhHIJUHtssgZXcs%2FVE51Gz2kS%2BJHz8G5VPlT%2FPzz%2FBQ%3D%3D&RelayState=YnsL8ZPGhfEoErqsS3vEpnEVp3Ckhhfm&SigAlg=http%3A%2F%2Fwww.w3.org%2F2001%2F04%2Fxmldsig-more%23rsa-sha256&Signature=juMhbPs0f9BeRWK96c6YFJ3ZmsLD5Cz3TOIopA2Kv3YfA5mP8rhreBb3AIU%2Be%2FU94z6iAa61bDgx7pM9dG2o%2FbkOVBuron%2FPrZQg5Flzrxw8Voivg9DWfH5gfKTd0JlrMI1bbYp6G%2F0dZV4pOQ04Ch9%2FNYvmBS%2BV9C2wkZn7T1jSppqRB8EmOisIJJZkObuxB4FrWwKj02FY%2BvO8qhMz8ibtMJePn4wTpMR%2F14TogUn6wAc6cgGsZ0Lg%2FGKlMsK6jZ3KgxKdcbZa3hrbZWyimuCuhZ%2FCNgxTb4AfZxsmpFrG8XNDaeXWNmV8BZHx2Mzpx7Fs5hoqz0dEWDMHBYHFlg%3D%3D")
    #Enter login info:
    #time.sleep(5)
    elementID = driver.find_element(By.ID,'okta-signin-username')
    elementID.send_keys(username)
    elementID = driver.find_element(By.ID, 'okta-signin-password')
    elementID.send_keys(password)
    elementID.submit()
    
    return

def select_correct_server(driver):
    
    select = Select(driver.find_element(By.ID, 'lstAuthType'))
    select.select_by_visible_text('NANOTECH61984 CLOUD AUTHENTICATION (NanoString)')
    button_element = driver.find_element(By.ID, 'btnLogin')
    button_element.click()
    return

def click_bluemountain(driver):
    blue_mountain_link = driver.find_element(By.XPATH, '/html/body/div[2]/div/section/main/div/section/section/section/section/section/div[3]/a').get_attribute('href')
    
    driver.get(blue_mountain_link)
    
    return

def bm_login(driver, username, password):
    #Open login page
    
    
    
    elementID = driver.find_element(By.ID,'okta-signin-username')
    elementID.send_keys(username)
    elementID = driver.find_element(By.ID, 'okta-signin-password')
    elementID.send_keys(password)
    elementID.submit()
    
    return

def scrape_bluemountain(driver, username, password):
    base_url = "https://nanostring.okta.com"
    time_to_sleep = 1
    max_results = 20
    driver.get(base_url)
    
    time.sleep(3)
    open_login(driver, username, password)
    time.sleep(6)
    click_bluemountain(driver)
    time.sleep(4)
    select_correct_server(driver)
    #Go to webpage
    time.sleep(4)
    bm_login(driver,username,password)
    
    time.sleep(2)
    pd_html=driver.page_source
    soup = BeautifulSoup(pd_html, 'html.parser')
    div = soup.select_one("div#itemList")
    df = pd.read_html(str(div))
    print(df.head())


    #datagrid = driver.find_element(By.ID, 'itemList:cg_tbl_body')
    # jobs_block= driver.find_element(By.CSS_SELECTOR, '.jobs-search-results__list')
    # jobs_list= jobs_block.find_elements(By.CSS_SELECTOR, '.jobs-search-results__list-item')
    # #of results
    # result_string = driver.find_element(By.CSS_SELECTOR, 'small.jobs-search-results-list__text').text
    # string_len_results = len(result_string)
    # result_string_trim = result_string[0:string_len_results-8]
    # result_count = int(result_string_trim.replace(",",""))
    # print("results count: " + str(result_count))
    # if result_count > max_results:
    #     result_count = max_results
    # initial_columns = ['Title', 'Company', 'Location', 'Link']

    # j = 0
    # df = pd.DataFrame(columns=initial_columns)
    # for i in range(0,result_count):
    #     elements = driver.find_elements(By.CSS_SELECTOR, '.jobs-search-results__list-item')
    #     driver.execute_script("arguments[0].scrollIntoView(true);", elements[j])
    #     time.sleep(time_to_sleep)
    #     df2 = pd.DataFrame(columns=initial_columns, data=[["title","company","location",'Link']])
    #     title = elements[j].find_element(By.CSS_SELECTOR, '.job-card-list__title').text
    #     company = elements[j].find_element(By.CSS_SELECTOR, '.job-card-container__company-name').text
    #     location = elements[j].find_element(By.CSS_SELECTOR, '.job-card-container__metadata-item').text
    #     link = elements[j].find_element(By.CSS_SELECTOR, '.job-card-list__title').get_attribute('href')
    #     df2.iloc[0] = [title,company,location,link]
    #     df = pd.concat([df,df2], ignore_index=True)
    #     j = j  + 1
    # print(df.head(15))

    # #Get page source code
    # src = driver.page_source
    # soup = BeautifulSoup(src, 'lxml')
    # company_html = soup.find_all('a', {'class': 'job-card-container__company-name'})
    # titles_html = soup.find_all('a', {'class': 'job-card-list__title'})
    # location_html = soup.find_all('a', {'class': 'job-card-container__metadata-item'})
    # job_titles = []
    # companies = []
