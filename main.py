from bs4 import BeautifulSoup
#import chrome webdriver
from selenium import webdriver
browser = webdriver.Chrome("chromedriver.exe")
username = "darrinbuenger@gmail.com"
password = str(input("Enter Password: "))

#Open login page
browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

#Enter login info:
elementID = browser.find_element_by_id('username')
elementID.send_keys(username)

elementID = browser.find_element_by_id('password')
elementID.send_keys(password)
#Note: replace the keys "username" and "password" with your LinkedIn login info
elementID.submit()
#Go to webpage
browser.get('https://www.linkedin.com/jobs/automation-engineer-jobs-greater-seattle-area/?geoId=90000091')
#Find search box
#jobID = browser.find_element_by_class_name('jobs-search-box__text-input')
#Send input
#jobID.send_keys(job)

#Get page source code
src = browser.page_source
soup = BeautifulSoup(src, 'lxml')
print(soup.prettify())
#Strip text from source code
results = soup.find('small', {'class': 'display-flex t-12 t-black--light t-normal'}).get_text().strip().split()[0]
results = int(results.replace(',', ''))
  
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
   
