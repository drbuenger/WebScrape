#import bs4
from bs4 import BeautifulSoup
#import chrome webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
#functions file import
import functions
from custom_classes import search_bundle
#import pandas
import pandas as pd
import time




time_to_sleep = 1
max_results = 20

username = "darrinbuenger@gmail.com"
password = str(input("Enter Password: "))

#initialize driver
#driver = webdriver.Chrome("chromedriver.exe")

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
prefs = {"credentials_enable_service": False,
     "profile.password_manager_enabled": False}
options.add_experimental_option("prefs", prefs)
#options.add_experimental_option("credentials_enable_service", False)
#options.add_experimental_option("profile.password_manager_enabled", False)
#service = ChromeService(executable_path=r"C:\Users\dbuenger\PycharmProjects\WebScrape\chromedriver.exe")
service = ChromeService(executable_path=r"C:\Users\darri\PycharmProjects\WebScrape\chromedriver.exe")


driver = webdriver.Chrome(service=service, options=options)


#build urls

base_url = "https://www.linkedin.com/"
search_url = "https://www.linkedin.com/jobs/search/?&keywords="

search = search_bundle
search.keywords = ["automation engineer", "process engineer"]
search.remove_words =["amazon", "meta", "microsoft", "google"]
search.locations = "United States"
urls=[]


urls = functions.create_urls(search_url, search)

functions.open_login(driver, username, password)

#Go to webpage
for url in urls:
    print(url)
    driver.get(url)
    #Find search box
    #jobID = browser.find_element_by_class_name('jobs-search-box__text-input')
    #Send input
    #jobID.send_keys(job)

    #functions.scroll_to_bottom(driver)
    time.sleep(2)
    functions.check_for_popups(driver)


    #Strip text from source code
    #titles_html = soup.find_all('a', {'class': 'full-width artdeco-entity-lockup__title ember-view'})
    jobs_block= driver.find_element(By.CSS_SELECTOR, '.jobs-search-results__list')
    jobs_list= jobs_block.find_elements(By.CSS_SELECTOR, '.jobs-search-results__list-item')

    #of results
    result_string = driver.find_element(By.CSS_SELECTOR, 'small.jobs-search-results-list__text').text
    #result_string = result_element.find_element(By.CLASS_NAME, 'small.jobs-search-results-list__text').text
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
    
    #print(job_titles)
#    print(companies)

#print(jobs_list)
   
#table = soup.find('a', attrs = {'class':'all_quotes'}) 
   
#table = soup.find('ul class', attrs = {'class':'jobs-search-results__list-item'}) 

# for row in table.findAll('div',
#                          attrs = {'class':'col-6 col-lg-3 text-center margin-30px-bottom sm-margin-30px-top'}):
#     quote = {}
#     quote['theme'] = row.h5.text
#     quote['url'] = row.a['href']
#     quote['img'] = row.img['src']
#     quote['lines'] = row.img['alt'].split(" #")[0]
#     quote['author'] = row.img['alt'].split(" #")[1]
#     quotes.append(quote)

# for row in table.findAll('div', attrs = {'class':'job-card-container'}):
#     df = pd.DataFrame()
#     text = row.h5.text