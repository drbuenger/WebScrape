import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


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
