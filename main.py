from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime
import os
import sys

# path to .exe script
executable_path = os.path.dirname(sys.executable)

now = datetime.now()
now_date = now.strftime("%H%M")

website = "https://g1.globo.com/"
path = "../chromedriver.exe"

# headless-mode for selenium (will run on background only)
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)
driver.get(website)

news_containers = driver.find_elements(by="xpath", value='//div[@class="feed-post-body"]')
titles = []
links = []

for container in news_containers:
    title = container.find_element(by="xpath", value='./div[2]/div/h2/a/p').text
    link = container.find_element(by="xpath", value='./div[2]/div/h2/a').get_attribute("href")

    titles.append(title)
    links.append(link)

df_dict = {"Titles": titles, "Link to article": links}
df_news = pd.DataFrame(df_dict)
file_name = f'news_{now_date}.csv'
df_news.to_csv(file_name)

driver.quit()
