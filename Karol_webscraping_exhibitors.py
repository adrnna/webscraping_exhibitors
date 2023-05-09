# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 11:30:52 2023

@author: adrnna
"""

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#establish the path to the driver and initialize it
driver = webdriver.Chrome()
#service = Service(executable_path=r'C:\Users\adpor\Desktop\Adu\programming\upwork\webscraping_exhibitors\chromedriver.exe')        #your chromedriver path goes here
#driver = webdriver.Chrome(service=service)
#wait for the site to load completely and maximize window
driver.implicitly_wait(10)
driver.maximize_window()
#open the website
driver.get("https://www.mwcbarcelona.com/exhibitors")
#accept cookies
accept_cookies = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
accept_cookies.click()
#function that goes through every link inside the table, when done goes to the next page and starts over
def page_nav():
    while True:
        try:
            # for each row: open the link in the same window, go back
            links = driver.find_elements(By.CSS_SELECTOR, ".whitespace-nowrap")
            for link in links:
                driver.execute_script("arguments[0].scrollIntoView();", link)
                time.sleep(1)
                driver.execute_script("arguments[0].click()", link)
                #print the title of the page just clicked, to make sure that everything is working properly
                get_title = driver.title
                print(get_title)
                driver.back()
            #when done with all links click on the 'next page' button
            next_page = driver.find_element(By.CSS_SELECTOR, '.ais-Pagination-item:last-child')
            driver.execute_script("arguments[0].scrollIntoView();", next_page)
            time.sleep(1)
            next_page.click()
            time.sleep(1)
        #on the last page an exception will be thrown
        except:
            print('End of document')
            break
page_nav()


