# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 11:50:29 2023

@author: adrnna
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

# Start a new instance of the Chrome browser
browser = webdriver.Chrome()

# Navigate to the website
browser.get("https://www.mwcbarcelona.com/exhibitors")

#cookies button
WebDriverWait(browser, 30).until(
    EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))) 
cookies_button = browser.find_element_by_id("onetrust-accept-btn-handler")
cookies_button.click()


class_name_ = "ais-ScrollTo"
element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name_)))

element1 = browser.find_element_by_class_name(class_name_)
browser.execute_script("arguments[0].scrollIntoView();", element1)
actions = ActionChains(browser)
actions.move_to_element(element).perform()
#click on the company 
companies = browser.find_elements_by_xpath("//tr[@class='flex px-4 cursor-pointer hover:bg-gray-100 sm:table-row sm:text-gray-700 sm:font-medium']/td[2]/div/h5")
company = browser.find_element_by_xpath("//tr[@class='flex px-4 cursor-pointer hover:bg-gray-100 sm:table-row sm:text-gray-700 sm:font-medium']/td[2]/div/h5")
# create action chain object
action = ActionChains(browser)
# perform the operation
action.move_to_element(company).perform()
action.move_to_element(company).click().perform()
#Go inside the exhibitor page description and scrape info

WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "exhibitor-container")))
exhibitor = browser.find_element_by_xpath("//h1").text
description = browser.find_element_by_xpath("//p").text
linkedin = browser.find_elements_by_xpath('//a[contains(@href, "%s")]' % "https://www.linkedin.com")[0].get_attribute('href')
web_child = browser.find_element_by_xpath("//span[contains(text(), 'Web')]")
web = web_child.find_element_by_xpath("..").get_attribute('href')


#Build dataframe
data = [{'Exhibitor': exhibitor,
        'Description': description,
        'Linkedin': linkedin,
        'Website': web}]
df = pd.DataFrame(data)