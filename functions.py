import time

def scroll_to_bottom(driver):
    start = time.time()
    
    # will be used in the while loop
    initialScroll = 0
    finalScroll = 1000
    
    while True:
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        # this command scrolls the window starting from
        # the pixel value stored in the initialScroll 
        # variable to the pixel value stored at the
        # finalScroll variable
        initialScroll = finalScroll
        finalScroll += 1000
    
        # we will stop the script for 3 seconds so that 
        # the data can load
        time.sleep(3)
        # You can change it as per your needs and internet speed
    
        end = time.time()
    
        # We will scroll for 20 seconds.
        # You can change it as per your needs and internet speed
        if round(end - start) > 20:
            break

def check_for_popups(driver):
    #Import exception check
    from selenium.common.exceptions import NoSuchElementException
    try:
        if driver.find_element_by_class_name('msg-overlay-list-bubble--is-minimized') is not None:
            pass
    except NoSuchElementException:
        try:
            if driver.find_element_by_class_name('msg-overlay-bubble-header') is not None:
                driver.find_element_by_class_name('msg-overlay-bubble-header').click()
        except NoSuchElementException:
            pass