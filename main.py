#import bs4
from bs4 import BeautifulSoup
#import chrome webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
#functions file import
import linkedin_functions
import bluemountain_functions

#import pandas
import pandas as pd
import time

which_site = str(input("Enter site choice: ")) 
username = str(input("Enter Username: "))
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
service = ChromeService(executable_path=r"C:\Users\dbuenger\PycharmProjects\WebScrape\chromedriver.exe")
#service = ChromeService(executable_path=r"C:\Users\darri\PycharmProjects\WebScrape\chromedriver.exe")


driver = webdriver.Chrome(service=service, options=options)

if which_site == "linkedin":
    #build urls
    linkedin_functions.scrape_linkedin(driver, username, password)

if which_site == "bluemountain":
    #build urls
    bluemountain_functions.scrape_bluemountain(driver, username, password)