import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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
    driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    #Enter login info:
    elementID = driver.find_element(By.ID,'username')
    elementID.send_keys(username)
    elementID = driver.find_element(By.ID, 'password')
    elementID.send_keys(password)
    elementID.submit()
    #Note: replace the keys "username" and "password" with your LinkedIn login info
    return

def create_urls(search_url,sb):
    urls =[]
    for keywords in sb.keywords:
        url = search_url
        format_keywords = keywords.replace(" ","%20")
        url += format_keywords
        url += "%20"
        for remove in sb.remove_words:
            url += "%20"
            url += "-" + remove
        for location in sb.locations:
            url += "&location=" + location.replace(" ", "%20")
            urls.append(url)
    return urls

def scrape_linkedin(driver, username, password):
    base_url = "https://www.linkedin.com/"
    search_url = "https://www.linkedin.com/jobs/search/?&keywords="
    max_results = 20
    time_to_sleep = 1


    search = search_bundle
    search.keywords = ["automation engineer", "process engineer"]
    search.remove_words =["amazon", "meta", "microsoft", "google"]
    search.locations = ["United States", "Greater Seattle Area"]
    urls=[]


    urls = create_urls(search_url, search)

    open_login(driver, username, password)

    #Go to webpage
    for url in urls:
        print(url)
        driver.get(url)
        time.sleep(2)
        check_for_popups(driver)
        jobs_block= driver.find_element(By.CSS_SELECTOR, '.jobs-search-results__list')
        jobs_list= jobs_block.find_elements(By.CSS_SELECTOR, '.jobs-search-results__list-item')
        #of results
        result_string = driver.find_element(By.CSS_SELECTOR, 'small.jobs-search-results-list__text').text
        string_len_results = len(result_string)
        result_string_trim = result_string[0:string_len_results-8]
        result_count = int(result_string_trim.replace(",",""))
        print("results count: " + str(result_count))
        if result_count > max_results:
            result_count = max_results
        initial_columns = ['Title', 'Company', 'Location', 'Link']

        j = 0
        df = pd.DataFrame(columns=initial_columns)
        for i in range(0,result_count):
            elements = driver.find_elements(By.CSS_SELECTOR, '.jobs-search-results__list-item')
            driver.execute_script("arguments[0].scrollIntoView(true);", elements[j])
            time.sleep(time_to_sleep)
            df2 = pd.DataFrame(columns=initial_columns, data=[["title","company","location",'Link']])
            title = elements[j].find_element(By.CSS_SELECTOR, '.job-card-list__title').text
            company = elements[j].find_element(By.CSS_SELECTOR, '.job-card-container__company-name').text
            location = elements[j].find_element(By.CSS_SELECTOR, '.job-card-container__metadata-item').text
            link = elements[j].find_element(By.CSS_SELECTOR, '.job-card-list__title').get_attribute('href')
            df2.iloc[0] = [title,company,location,link]
            df = pd.concat([df,df2], ignore_index=True)
            j = j  + 1
        print(df.head(15))

        #Get page source code
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        company_html = soup.find_all('a', {'class': 'job-card-container__company-name'})
        titles_html = soup.find_all('a', {'class': 'job-card-list__title'})
        location_html = soup.find_all('a', {'class': 'job-card-container__metadata-item'})
        job_titles = []
        companies = []

        for title in titles_html:
            job_titles.append(title.text.strip())
        
        for company in company_html:
            companies.append(company.text.strip())