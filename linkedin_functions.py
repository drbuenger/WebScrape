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
        try:
            driver.find_element(By.CLASS_NAME,'msg-overlay-bubble-header__details').find_element(By.CLASS_NAME, "msg-overlay-bubble-header__button").click()
        except:
            print("no minimize button found during check for popups")
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
    return

def create_urls(search_url,sb):
    search_name = {}
    urls =[]
    date_modifiers =[]
    for days in sb.date_posted:
        seconds = int(days) * 24 * 60 * 60
        date_filter = 'f_TPR=r' + str(seconds)
        date_modifiers.append(date_filter)
    for keywords in sb.keywords:
        url = search_url
        format_keywords = keywords.replace(" ","%20")
        url += format_keywords
        url += "%20"
        for remove in sb.remove_words:
            url += "%20"
            url += "-" + remove
        for location in sb.locations:
            location_url = url + "&location=" + location.replace(" ", "%20")
            search_name[location_url] = keywords + "_" + location
            urls.append(location_url)
       

    return urls, date_modifiers, search_name

def scrape_linkedin(driver, username, password):
    base_url = "https://www.linkedin.com/"
    search_url = base_url + "jobs/search/?&keywords="
    max_results = 100
    page_size = 25
    time_to_sleep = 1

    search = search_bundle
    search.keywords = [
        "Senior Automation Engineer",
        "IT MES Engineer",
        # "Manufacturing Analytics Manager",
        # "MS and T Process Automation",
        # "Senior Manufacturing Engineer",
        ]
    search.remove_words =["amazon", "meta", "microsoft", "google", 'blue origin', 'dice']
    search.locations = ["Greater Seattle Area"]
    search.date_posted = [
        '7',
         '1',
         ]
    urls=[]

    urls, date_modifiers, search_name = create_urls(search_url, search)

    open_login(driver, username, password)

    #Go to webpage(s)
    for url in urls:
        for date in date_modifiers:
            page_count = 1
            page_result_max = page_size * page_count

            #initial page
            print(url)
            driver.get(url)
            time.sleep(2)
            check_for_popups(driver)
            # call same page, but with the time filter on (must be called without filter first, then with filter)
            url_modified = url.replace("&keywords=", date + '&keywords=')
            driver.get(url_modified)
            check_for_popups(driver)
            jobs_block= driver.find_element(By.CSS_SELECTOR, '.jobs-search-results-list')
            jobs_list= jobs_block.find_elements(By.CSS_SELECTOR, '.job-card-list__entity-lockup')
            #of results
            try:
                result_string = driver.find_element(By.CSS_SELECTOR, 'small.jobs-search-results-list__text').text
                string_len_results = len(result_string)
                result_string_trim = result_string[0:string_len_results-8]
                result_count = int(result_string_trim.replace(",",""))
                print("results count: " + str(result_count))
                if result_count > max_results:
                    result_count = max_results
                initial_columns = ['Title', 'Company', 'Location', 'Link']
                if page_result_max > max_results:
                    page_result_max = max_results
                df = pd.DataFrame(columns=initial_columns)
                for x in range(0, result_count):
                    page_result_max = page_size * page_count
                    if x >0:
                        # reload with next page
                        new_url = url + "&start=" + str((page_count-1)*page_size)
                        print(new_url)
                        driver.get(new_url)
                        time.sleep(2)
                        check_for_popups(driver)
                        # call same page, but with the time filter on (must be called without filter first, then with filter)
                        url_modified = new_url.replace("&keywords=", date + '&keywords=')
                        driver.get(url_modified)
                        check_for_popups(driver)
                    for i in range(0,page_result_max):
                        elements = driver.find_elements(By.CSS_SELECTOR, '.jobs-search-results__list-item')
                        driver.execute_script("arguments[0].scrollIntoView(true);", elements[i])
                        time.sleep(time_to_sleep)
                        df2 = pd.DataFrame(columns=initial_columns, data=[["title","company","location",'Link']])
                        try:
                            title = elements[i].find_element(By.CSS_SELECTOR, '.job-card-list__title').text
                        except:
                            title = "Not Found"
                        try:
                            company = elements[i].find_element(By.CSS_SELECTOR, '.job-card-container__company-name').text
                        except:
                            company = "Not Found"
                        try:
                            location = elements[i].find_element(By.CSS_SELECTOR, '.job-card-container__metadata-item').text
                        except:
                            location = "Not Found"
                        try:
                            link = elements[i].find_element(By.CSS_SELECTOR, '.job-card-list__title').get_attribute('href')
                        except:
                            link = "Not Found"
                        df2.iloc[0] = [title,company,location,link]
                        df = pd.concat([df,df2], ignore_index=True)
                    page_count = page_count + 1
                
                print(df.head(15))
                file_name = search_name[url] + "_" + date
                df.to_csv(file_name, index=False, header=True)
            except:
                continue

            # #Get page source code
            # src = driver.page_source
            # soup = BeautifulSoup(src, 'lxml')
            # company_html = soup.find_all('a', {'class': 'job-card-container__company-name'})
            # titles_html = soup.find_all('a', {'class': 'job-card-list__title'})
            # location_html = soup.find_all('a', {'class': 'job-card-container__metadata-item'})
            # job_titles = []
            # companies = []

            # for title in titles_html:
            #     job_titles.append(title.text.strip())
            
            # for company in company_html:
            #     companies.append(company.text.strip())