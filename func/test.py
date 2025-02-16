from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import re
# Function to perform a Google search and extract links
classes = set()
classes= {"zCubwf","hgKElc","LTKOO sY7ric","Z0LcW","gsrt vk_bk FzvWSb YwPhnf","pclqee","tw-Data-text tw-text-small tw-ta",
    "IZ6rdc","O5uR6d LTKOO","vlzY6d","webanswers-webanswers_table__webanswers-table",
    "dDoNo ikb4Bb gsrt","sXLaOe","LWkfKe","VQF4g","qv3Wpe","kno-rdesc","SPZz6b",'myclasses',
    "rPeykc","Yh5dPc"
}
new_classes = set(["vk_gy vk_sh card-section sL6Rbf","rPeykc","Yh5dPc","VQF4g","hgKElc"])
classes = classes.union(new_classes)

def search(query):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    # sanitize the query
    query.replace('+',' plus ').replace('-',' minus ')
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    driver.get(url)
    time.sleep(5) # waiting time for pages to load

    for class_name in classes:
        try:
            element = driver.find_element(By.CLASS_NAME, class_name)
            result = element.text.strip()

            if result:
                print(f"Found at \033[32m{class_name}\033[0m")
                driver.quit()
                return result
        except:
            pass
    driver.quit()
    return None

while(True):
    query = input("Enter search query : ")
    print(search(query))