import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import unittest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pytest
from selenium.webdriver.common.alert import Alert 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
# Creating Chrome Webdriver Instance
# chrome_options = Options()
# chrome_options.add_argument("--headless")

# Initialising WebDriver with Chrome options
driver = webdriver.Chrome(options=chrome_options)

# Navigating to the URL
driver.maximize_window()
driver.get("https://dev.infyni.com/")
courseNum=1
# time.sleep(3)
driver.find_element(By.XPATH,f'//div[2]/div[2]/div[{courseNum}]/div/div[2]/div[2]/a[text()="Enroll Now "]').click()
wait=WebDriverWait(driver,10)
element = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
element.send_keys('panda11@mailinator.com')
# driver.find_element(By.XPATH,'//input[@name="username"]').send_keys('panda11@mailinator.com')
driver.find_element(By.XPATH,'//input[@name="password"]').send_keys('panda11')
driver.find_element(By.CSS_SELECTOR,'.col-md-12 > .butn').click()
textdata=driver.find_element(By.CSS_SELECTOR,'div.page-title-box>h4').get_attribute('textContent')
print(f"textdata is {textdata}")
assert textdata == "Course Details","not matched"
driver.find_element(By.XPATH,'//span[text()="Dashboard  "]').click()
driver.find_element(By.LINK_TEXT,'Join Live Session').click()
# time.sleep(5)
# driver.switch_to.frame(0)
# driver.find_element(By.XPATH,'//*[@id="app"]/div[2]/div/div[2]/div[1]/div/div[2]/div/div/div/div[2]/button/div').click()
# alert = Alert(driver)
# alert.accept()
original_tab = driver.current_window_handle
driver.find_element(By.XPATH,'//button[text()="Go To Dashboard"]/parent::a').click()
all_tabs = driver.window_handles
for tab in all_tabs:
    if tab != original_tab:
        driver.switch_to.window(tab)
        break

driver.find_element(By.XPATH,'//nav/ul[1]/li[7]/a').click()
driver.find_element(By.XPATH,'//span[text()="Logout"]').click()
driver.switch_to.window(original_tab)
driver.find_element(By.XPATH,'//button[text()="Go To Dashboard"]/parent::a').click()
time.sleep(100)
