#import chrome webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
#functions file import
import linkedin_functions


#username = str(input("Enter Username: "))
username = "darrinbuenger@gmail.com"
password = str(input("Enter Password: "))

#initialize driver
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
prefs = {"credentials_enable_service": False,
     "profile.password_manager_enabled": False}
options.add_experimental_option("prefs", prefs)
service = ChromeService(executable_path=r"C:\Users\dbuenger\source\repos\WebScrape\chromedriver.exe")
#service = ChromeService(executable_path=r"C:\Users\darri\source\repos\WebScrape\chromedriver.exe")

driver = webdriver.Chrome(service=service, options=options)

linkedin_functions.scrape_linkedin(driver, username, password)

