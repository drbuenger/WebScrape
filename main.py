#import bs4
from bs4 import BeautifulSoup
#import chrome webdriver
from selenium import webdriver
#functions file import
import functions
username = "darrinbuenger@gmail.com"
password = str(input("Enter Password: "))

#initialize driver
driver = webdriver.Chrome("chromedriver.exe")

#Open login page
driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

#Enter login info:
elementID = driver.find_element_by_id('username')
elementID.send_keys(username)

elementID = driver.find_element_by_id('password')
elementID.send_keys(password)
#Note: replace the keys "username" and "password" with your LinkedIn login info
elementID.submit()
#Go to webpage
driver.get('https://www.linkedin.com/jobs/automation-engineer-jobs-greater-seattle-area/?geoId=90000091')
#Find search box
#jobID = browser.find_element_by_class_name('jobs-search-box__text-input')
#Send input
#jobID.send_keys(job)

functions.check_for_popups(driver)
functions.scroll_to_bottom(driver)

#Get page source code
src = driver.page_source
soup = BeautifulSoup(src, 'lxml')
#Strip text from source code
#titles_html = soup.find_all('a', {'class': 'full-width artdeco-entity-lockup__title ember-view'})
company_html = soup.find_all('a', {'class': 'job-card-container__company-name'})
titles_html = soup.find_all('a', {'class': 'job-card-list__title'})
job_titles = []
companies = []
for title in titles_html:
    job_titles.append(title.text.strip())

 
for company in company_html:
    companies.append(company.text.strip())
  
print(job_titles)
print(companies)
#results = int(results.replace(',', ''))
  
# soup = BeautifulSoup(r.content, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib
# print(soup.prettify())
   
# table = soup.find('div', attrs = {'id':'all_quotes'}) 
   
# for row in table.findAll('div',
#                          attrs = {'class':'col-6 col-lg-3 text-center margin-30px-bottom sm-margin-30px-top'}):
#     quote = {}
#     quote['theme'] = row.h5.text
#     quote['url'] = row.a['href']
#     quote['img'] = row.img['src']
#     quote['lines'] = row.img['alt'].split(" #")[0]
#     quote['author'] = row.img['alt'].split(" #")[1]
#     quotes.append(quote)