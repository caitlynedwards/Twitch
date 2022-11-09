#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 11:57:57 2020

@author: caitlynedwards
"""
  
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 08:03:51 2019
Last Updated: July 22nd
@author: cpollack
"""

#%% Importing Libraries

# other imports
import configparser
import time
import pandas as pd
import os
import ipdb

# selenium specific imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException    


from MisspellingsList import words


#%% Initial Configuration 

# configuration parser initialization
config = configparser.ConfigParser()
config.read('./config.ini')
delay = 10 # waits for 10 seconds for the correct element to appeaar

#%% Read in File

stream_data = pd.DataFrame(columns=['Word', 'Streamer', 'Message', 'Time', 'Channel', 'Game', 'Language', 'Viewers'])

#%% Login

def login_streamhatchet():
    driver.get("https://app.streamhatchet.com/")
    time.sleep(3) # sleep for 3 seconds to let the page load
    #driver.find_element_by_id("hs-eu-confirmation-button").click()

    username = driver.find_element_by_name("loginEmail")
    username.clear()
    username.send_keys(config['login_credentials']['email'])

    password = driver.find_element_by_name("loginPassword")
    password.clear()
    password.send_keys(config['login_credentials']['password'])

    driver.find_element_by_xpath("//button[contains(text(),'Login')]").click()
    time.sleep(3) # sleep for 3 seconds to let the page load

#%% 
def run_search():
    df = []
    
    # To help wait for data to load on the page, we wait until we can see Messages Count
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//p[@id='messages-count']")))
    
    table_rows = driver.find_elements_by_xpath("//table[@id='table_discovery']/tbody/tr")
    
    for i in table_rows:
        td_data = []
        for td in i.find_elements_by_tag_name("td"):
            td_data.append(td.text)
        df.append(td_data)

    return(df)


#%% Stream Chat Search
def stream_chat_search(query, streamer):
    driver.get("https://app.streamhatchet.com/chatsearch")
    time.sleep(1)
    
    # Enters query into 'Stream title query'
    stream_title_query_input = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='chat-query']")))
    stream_title_query_input.send_keys(query)
    
    # Click to Check Statistics Box
    driver.find_element_by_xpath("//div[@class = 'checkbox']").click()

#pick a specific streamer
    driver.find_element_by_xpath("//div[@class='selectize-input items not-full']").click()
    driver.find_element_by_xpath("//div[@class='selectize-input items not-full focus input-active']").click()
    select_streamer = driver.find_element_by_id("streamSearcher-selectized")
    select_streamer.send_keys(streamer[0])
    #ipdb.set_trace()
    #Myth - 110690086
    #Flight23White - 51270104
    #ITSHAFU- 30777889
    #XCHOCOBARS - 42583390
    #TFUE - 60056333
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//div[@class='selectize-dropdown-content']")))
    driver.find_element_by_xpath("//div[@data-value='{}']".format(streamer[1])).click()

    # Click to Expand Date Options
    driver.find_element_by_xpath("//div[@id='NewRangePicker']").click()
    
    #  # Select last 30 days
    #driver.find_element_by_css_selector("div#new-picker > div.ranges > ul > li:nth-child(3)").click()
    #Select specific Day
    driver.find_element_by_xpath("//div[@class='calendar left']//td[@data-title='r2c0']").click()
    driver.find_element_by_xpath("//div[@class='calendar left']//td[@data-title='r2c6']").click()
    
    driver.find_element_by_xpath("//button[@class='applyBtn btn btn-sm btn-success ui google plus button']").click()
    run_button = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='medium ui google plus submit button']")))
    run_button.click()
    time.sleep(4)
    
     # Click to Download CSV
   # driver.find_element_by_xpath("//div[@id='exportDiscovery']").click()
    
    # # Apply filters
    # driver.find_element_by_id("submitDiscovery").click()
        
    return(run_search())


#%% Test Case
# df = []

# driver = webdriver.Chrome(executable_path = os.path.abspath("chromedriver")) #Open chrome driver so that it opens in another page
# login_streamhatchet()
# num_titles, unique_channels, unique_users, table_id = stream_title_search("test", df) #Run above script

#%% Run Stream Title Search

driver = webdriver.Chrome(executable_path = os.path.abspath("chromedriver")) #Open chrome driver so that it opens in another page

login_streamhatchet() #Log into streamhatchet
# List of streamers
streamers = [
    ["MYTH", 110690086],
    ["Flight23White", 51270104],
    ["ITSHAFU", 30777889],
    ["XCHOCOBARS", 42583390],
    ["TFUE", 60056333]]

for word in words: #For each word
    print("Starting " + word) #Print so you know which line you're on
    for streamer in streamers:
        tries = 3
        for try_num in range(tries):
            try:
                table_id = stream_chat_search(word, streamer) #Run above script
            except TimeoutException:
                if try_num < tries - 1:
                    continue
                else:
                    print("Too many Timeouts for word: {} and streamer: {}".format(word, streamer[0]))
            break

        if len(table_id[0]) == 1: #If no data
                stream_data = stream_data.append({'Word': word,
                                                  'Streamer': streamer[0],
                                                  'Message': "None", #Adds unique users, streamers, and total views to data set
                                                  'Time': "None",
                                                  'Channel': "None",
                                                  'Game': "None",
                                                  'Language': "None", 
                                                  'Viewers': 0}, ignore_index = True)
        else: #If at least one stream title
            for i in range(len(table_id)): #For table of results
                stream_data = stream_data.append({'Word': word,
                                                  'Streamer': streamer[0],
                                                  'Message': table_id[i][0], #Adds unique users, streamers, and total views to data set
                                                  'Time': table_id[i][1],
                                                  'Channel': table_id[i][2],
                                                  'Game': table_id[i][3],
                                                  'Language': table_id[i][4], 
                                                  'Viewers': table_id[i][5]}, ignore_index = True)


#%% Export Data File
stream_data.to_csv('/Users/caitlynedwards/Desktop/python/Keally_WeekAfter_100ChatMessages_5Streamers.csv', index = None, header=True)

