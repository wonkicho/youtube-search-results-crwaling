from selenium import webdriver
from selenium.common.exceptions import WebDriverException as WDE
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from pytube import YouTube
import time
import pandas as pd
import math

def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, 99999)")
    time.sleep(1)

url = "https://youtube.com/"
download_folder = r"C:\Users\chowk\Desktop\trailers"
keyword = "영화 예고편"
finish_line = 10000
count = 100


start_time = time.time()
path = 'C:\project\youtube_crwal\chromedriver.exe'
browser = webdriver.Chrome(path) 
browser.maximize_window()
browser.get("https://www.youtube.com/results?search_query={}&sp=EgQQARgB".format(keyword))

for i in range(math.ceil((count-26)/20)):
    scroll_down(browser)
    
crawling_list = []
url_list = []

# url 수집
crawling_list = browser.find_elements_by_tag_name('h3 > a')

for crawling in crawling_list:
    url = crawling.get_attribute('href')   
    url_list.append(url)
browser.close()
url_list = url_list[:count]

sec_list = []
title_list = []
for i in range(len(url_list)):
    yt = YouTube(url_list[i])
    stream = yt.streams.get_highest_resolution()
    stream.download(download_folder)
    sec_list.append(yt.length)
    title_list.append(yt.title)
    
df = pd.DataFrame({"title": [title_list], "time(sec)" : [sec_list]})
df.to_csv(r"C:\project\youtube_crwal" + "metadata.csv")
end_time = time.time()
finish = end_time - start_time
print(f"total time : {finish}")
