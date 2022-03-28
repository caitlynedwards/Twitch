#!/usr/bin/env python3
# -*- coding: utf-8 -*

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


# %% Read in data files
words = pd.read_csv("Brands.csv", header = None, encoding = "latin-1").dropna() #Import brand list compiled by Travis
# words = words.dropna() #Drop any NAs

words = words.values.tolist()
words = list(map(''.join, words))

#%% Initial Configuration 

# configuration parser initialization
config = configparser.ConfigParser()
config.read('./config.ini')
delay = 10 # waits for 10 seconds for the correct element to appeaar

#%% Read in File

stream_data = pd.DataFrame(columns=['Word', 'Titles', 'Unique Channels', 'Hours Watched', 'Airtime'])

#%% Login

def login_streamhatchet():
    driver.get("https://app.streamhatchet.com/")
    time.sleep(5) # sleep for 3 seconds to let the page load
    #driver.find_element_by_id("hs-eu-confirmation-button").click()

    username = driver.find_element_by_name("loginEmail")
    username.clear()
    username.send_keys(config['login_credentials']['email'])

    password = driver.find_element_by_name("loginPassword")
    password.clear()
    password.send_keys(config['login_credentials']['password'])

    driver.find_element_by_xpath("//button[contains(text(),'Login')]").click()
    time.sleep(3) # sleep for 3 seconds to let the page load

#%% Stream Title Search
def stream_title_search(query):
    driver.get("https://app.streamhatchet.com/streamtitles")
    time.sleep(1)
    
    # Enters query into 'Stream title query'
    stream_title_query_input = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//input[@id='status-query']")))
    stream_title_query_input.send_keys(query)

    # Makes twitch the only platform to search
    platform_input = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//input[@class='search']")))
    platform_input.click()
    for x in range(0,13):
        platform_input.send_keys(Keys.BACKSPACE)
    
     ###   Makes Facebook the only platform to search
    # platform_input = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//input[@class='search']")))
    # platform_input.click()
    # driver.find_element_by_xpath("//a[@data-value='twitch']//i[@class='delete icon']").click()
    # driver.find_element_by_xpath("//a[@data-value='ytg']//i[@class='delete icon']").click()
    # driver.find_element_by_xpath("//a[@data-value='mixer']//i[@class='delete icon']").click() 
    # for x in range(0,10):
    #     platform_input.send_keys(Keys.BACKSPACE)
    
    
    #         # Makes Youtube the only platform to search
    # platform_input = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//input[@class='search']")))
    # platform_input.click()
    # driver.find_element_by_xpath("//a[@data-value='twitch']//i[@class='delete icon']").click()
    # #driver.find_element_by_xpath("//a[@data-value='ytg']//i[@class='delete icon']").click()
    # driver.find_element_by_xpath("//a[@data-value='mixer']//i[@class='delete icon']").click() 
    # for x in range(0,11):
    #     platform_input.send_keys(Keys.BACKSPACE)

    # Click to Expand Date Options
    driver.find_element_by_xpath("//div[@id='NewRangePicker']").click()
    
    # change the hours and minutes to 0:00 for date from and to 
    driver.find_element_by_xpath("//div[@class='calendar left']//select[@class='hourselect']//option[1]").click()
    driver.find_element_by_xpath("//div[@class='calendar left']//option[contains(text(),'00')]").click()
    driver.find_element_by_xpath("//div[@class='calendar right']//select[@class='hourselect']//option[1]").click()
    driver.find_element_by_xpath("//div[@class='calendar right']//option[contains(text(),'00')]").click()
    
    #July 2019 - 0,14; left']//tr[1]//td[2]; left r4c3
    #Aug 2019 13, left 1 5; 4 6
    #Sept 2019 12, 2 1; 5 1
    #Oct 2019 11, 1 3; 4 4 
    #Nov 2019 - 10, 1 6; 4 6
    #Dec 2019 - 9; 2 1; 5 2
    #Jan 2020 - 8; 1 4; 4 5
    #Feb 2020 - 7; 1 7; 4 6
    #Mar 2020 - 6' 2 1; 5 2
    #April 2020 - 5; 1 4; 4 4
    #May 2020 - 4; 1 6; 5 0
    #June 2020 - 3; 1 2; 4 2
    #July 2020 - 2, 1 4; 4 5
    #Aug 2020 - 1; 1 7; 
    #sep 2020 - 1; right 1 3; right 1 3
    # Keep clicking on left_arrow
    for x in range(0,2):
    #     #while driver.find_element_by_xpath("//i[@id='icon-down-New']").is_displayed() == True:
         try:
             driver.find_element_by_xpath("//i[@class='fa fa-chevron-right glyphicon glyphicon-chevron-right']").click()
         except:
             break
    #driver.find_element_by_xpath("//i[@class='fa fa-chevron-right glyphicon glyphicon-chevron-right']").click()
                
     # Click on first day of the month:  
    #ipdb.set_trace()
    day_one_element = driver.find_element_by_xpath("//div[@class='calendar right']//tr[1]//td[3]")
    try:
        day_one_element.click()
    except WebDriverException:
        print("First Day element is not clickable")   
    
    # while driver.find_element_by_xpath("//i[@id='icon-down-New']").is_displayed() == True:
    #     try:
    #         driver.find_element_by_xpath("//i[@class='fa fa-chevron-right glyphicon glyphicon-chevron-right']").click()
    #     except:
    #        break
    
    driver.find_element_by_xpath("//div[@class='calendar right']//td[@data-title='r1c6']").click()

    # Runs the search
    driver.find_element_by_xpath("//button[@class='applyBtn btn btn-sm btn-success ui google plus button']").click()
    run_button = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='medium ui google plus submit button']")))
    run_button.click()
    
    # Scrape the Number of Titles
    num_titles = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//p[@id='messages-count']")))
    num_titles = num_titles.text
    #print(num_titles)
    
    unique_channels = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//p[@id='messages-uniquechannels']")))
    unique_channels = unique_channels.text
    #print(unique_channels)
    
    hours_watched = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//p[@id='messages-hourswatched']")))
    hours_watched = hours_watched.text
   # print(hours_watched)
  
    messages_airtime = WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//p[@id='messages-airtime']")))
    messages_airtime = messages_airtime.text
    #print(messages_airtime) 
    
  
    # #Scrolling to bottom of page to pull table data
    # last_height = driver.execute_script("return document.body.scrollHeight")
    # prev_num_rows = 0
    # while True:
    #     #Scroll down to bottom

    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
    
    #     #Wait to load page
    #     time.sleep(4)
    #     table_rows = driver.find_elements_by_xpath("//table[@id='table_discovery']/tbody/tr")
    #     num_rows = len(table_rows)
    #     print("NUMBER OF ROWS: ---> " + str(num_rows))
    #     for i in range(prev_num_rows, num_rows):
    #         df.append(table_rows[i].text.split("\n"))
        
    #     #Calculate new scroll height and compare with last scroll height
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height
    #     prev_num_rows = num_rows
    
   # WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH,"//table[@id='table_discovery']/tbody/tr")))

    # Pulls table data
    # table_rows = driver.find_elements_by_xpath("//table[@id='table_discovery']/tbody/tr")
    # #df = [i.text for i in table_rows]
    # ipdb.set_trace()
    # print("Number of ROWS: " + str(len(table_rows)))
    # for i in table_rows:
    #     df.append(i.text.split("\n"))
    #for 
    #print(driver.find_element_by_xpath("//table/tbody"))#.split("\n")
   
    #print(driver.find_element_by_xpath("//table/tbody").text)#.split("\n")

    #df = driver.find_element_by_id("table_discovery").text.split(",")
    #df = driver.find_element_by_xpath("//*[@id='table_discovery']").text.split("t")

    return(num_titles, unique_channels, hours_watched, messages_airtime)

#%% Run Stream Title Search

driver = webdriver.Chrome(executable_path = os.path.abspath("chromedriver")) #Open chrome driver so that it opens in another page
#driver = webdriver.Chrome(executable_path = /Users/caitlynedwards/desktop/python/chromedriver.exe)) #Open chrome driver so that it opens in another page

login_streamhatchet() #Log into streamhatchet

for word in words: #For each word
    print("Starting " + word) #Print so you know which line you're on
    tries = 3
    for try_num in range(tries):
        try:
            statistics = stream_title_search(word) #Run above script
        except TimeoutException:
            if try_num < tries - 1:
                continue
            else:
                statistics = ["Timed Out", "Timed Out", "Timed Out", "Timed Out", "Timed Out"]
                print("Too many Timeouts for word: {}".format(word))
        break
    #statistics = stream_title_search(word) #Run above script
    #print(range(len(table_id))[0::8])
    #for i in range(len(table_id))[0::8]: #For table of results, where [0::n], n is number of columns
    
    stream_data = stream_data.append({'Word': word,
                                      'Titles': statistics[0], #Adds unique users, streamers, and total views to data set
                                      'Unique Channels': statistics[1], 
                                      'Hours Watched': statistics[2],
                                      'Airtime': statistics[3]}, ignore_index = True)

#%% Export Data File
stream_data.to_csv('/Users/caitlynedwards/Desktop/python/StreamTitles_Twitch_Dec_2020_HotPocket.csv', index = None, header=True)
