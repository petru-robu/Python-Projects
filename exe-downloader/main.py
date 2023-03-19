import requests
import bs4
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import urllib

#https://wildbit-soft.fi/download/dev/6_9/ViewerSetup.exe


url = 'https://wildbit-soft.fi/download/dev/6_9/ViewerSetup.exe'

filename = 'download.exe'  
urllib.request(url, filename)



'''
browser = webdriver.Firefox()

browser.get('http://www.youtube.com')
assert 'YouTube' in browser.title

elem = browser.find_element(By.ID, 'search-input')  # Find the search box
elem.send_keys('test' + Keys.RETURN)

browser.quit()'''