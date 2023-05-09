# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 16:56:56 2023

@author: adrnna
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time 

# Start a new instance of the Chrome browser
browser = webdriver.Chrome()

# Navigate to the website
browser.get("https://www.mwcbarcelona.com/exhibitors")
# Store the ID of the original window
original_window = browser.current_window_handle

#cookies - wait and click
WebDriverWait(browser, 30).until(
    EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))) 
cookies_button = browser.find_element_by_id("onetrust-accept-btn-handler")
cookies_button.click()

#wait until loaded 
class_name_ = "ais-ScrollTo"
exhibitors, descriptions, linkedins, webs = ([] for i in range(4))

while True:

    #how many exhibitors
    WebDriverWait(browser, 5).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, class_name_)))
    time.sleep(1)
    companies = (browser.find_elements_by_xpath("//tr[@class='flex px-4 cursor-pointer hover:bg-gray-100 sm:table-row sm:text-gray-700 sm:font-medium']/td[2]/div/h5"))
    number_companies = len(companies)
    
    
    for i in range (number_companies):
        time.sleep(1)
        companies_click = (browser.find_elements_by_xpath("//tr[@class='flex px-4 cursor-pointer hover:bg-gray-100 sm:table-row sm:text-gray-700 sm:font-medium']/td[2]/div/h5"))
        time.sleep(1)
        element = WebDriverWait(browser, 5).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, class_name_)))
        
        #scroll down 
        element1 = browser.find_element_by_class_name(class_name_)
        browser.execute_script("arguments[0].scrollIntoView();", companies_click[i])
        time.sleep(1)
               
        # create action chain object
        action = ActionChains(browser)
        time.sleep(1)
        ActionChains(browser).key_down(Keys.CONTROL).click(companies_click[i]).key_up(Keys.CONTROL).perform()
        
        #Go inside the exhibitor page description and scrape info
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "exhibitor-container")))
        #EXHIBITORS
        try:
            exhibitor = browser.find_element_by_xpath("//h1").text
        except:
            exhibitor = "NO DATA"
        finally:
            exhibitors.append(exhibitor)
        #DESCRIPTIONS
        try:
            description = browser.find_element_by_xpath("//p").text
        except:
            description = "NO DATA"
        finally:
            descriptions.append(description)
        #LINKEDIN
        try:
            linkedin = browser.find_elements_by_xpath('//a[contains(@href, "%s")]' % "https://www.linkedin.com")[0].get_attribute('href')
        except:
            linkedin = "NO DATA"
        finally:
            linkedins.append(linkedin)
        #WEBS
        try:
            web_child = browser.find_element_by_xpath("//span[contains(text(), 'Web')]")
            web = web_child.find_element_by_xpath("..").get_attribute('href')
        except:
            web = "NO DATA"
        finally:
            webs.append(web)
        print(exhibitor, linkedin, web)
        time.sleep(2)
        browser.back()
        time.sleep(2)
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name_)))
    
    #GO TO THE NEXT PAGE
    next_page_button = browser.find_element(By.CSS_SELECTOR, '.ais-Pagination-item:last-child')
    browser.execute_script("arguments[0].scrollIntoView();", next_page_button)
    time.sleep(2)
    next_page_button.click()
    print("\nNEXT PAGE\n")
    time.sleep(2)

    
#Build dataframe
df = pd.DataFrame(list(zip(exhibitors, descriptions, linkedins, webs)), 
                  columns = ['Exhibitor', 'Description', 'Linkedin', 'Website'])