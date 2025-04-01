from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from requests import get as Rget, ConnectionError
import time
import sys
import re
import SpeakOffline as SOF
# New changes
import undetected_chromedriver as uc
# Function to perform a Google search and extract links
classes = set()
classes= {"zCubwf","hgKElc","LTKOO sY7ric","Z0LcW","gsrt vk_bk FzvWSb YwPhnf","pclqee","tw-Data-text tw-text-small tw-ta",
    "IZ6rdc","O5uR6d LTKOO","vlzY6d","webanswers-webanswers_table__webanswers-table",
    "dDoNo ikb4Bb gsrt","sXLaOe","LWkfKe","VQF4g","qv3Wpe","kno-rdesc","SPZz6b",'myclasses',
    "rPeykc","Yh5dPc"
}
new_classes = set(["vk_gy vk_sh card-section sL6Rbf","rPeykc","Yh5dPc","VQF4g","hgKElc","kno-rdesc","YpjmDb LLotyc","vk_bk dDoNo FzvWSb","Ww4FFb vt6azd","vk_bk dDoNo FzvWSb"])
classes = classes.union(new_classes)

def make_google_search(query, max_results=2):
    # nested function to extract domain name
    def extract_domain(url):
        pattern = r"(https?://)?(www\d?\.)?(?P<domain>[\w\.-]+\.\w+)(?:/\S*)?"
        match = re.match(pattern, url)
        if match:
            domain = match.group("domain")
            return domain
        return None

    def check_connection(url):
        try:
            response = Rget(url, timeout=5)
            return True
        except ConnectionError:
            return False
    # check for internet connection
    if not check_connection('https://www.google.com'):
        SOF.Speak('Please check your internet connection ...')
        return None
    # options = webdriver.ChromeOptions()
    options = Options()
    # options.add_argument("--headless=new")  # Improved headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.headless = True
    # driver = webdriver.Chrome(options=options)
    driver = uc.Chrome(options=options)
    # sanitize the query
    query.replace('+',' plus ').replace('-',' minus ')
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    driver.get(url)
    time.sleep(5) # waiting time for pages to load
    #-----------------------------------------------------------
    for class_name in classes:
        # print(f'\033[32m{class_name}\033[0m')
        try:
            element = driver.find_element(By.CLASS_NAME, class_name)
            result = element.text.strip()

            if result:
                print(f"Found at \033[32m{class_name}\033[0m")
                driver.quit()
                SOF.Speak(result)
                return result
        except:
            pass
    #-----------------------------------------------------------
    SOF.Speak(f"Searching websites for {query}")
    time.sleep(3)  # Gives time for search results to load
    # XML Path for complexing matching
    results = driver.find_elements(By.XPATH, "//div[@class='tF2Cxc']//a")
    links = [result.get_attribute("href") for result in results[:max_results]]
    # quit the driver
    # driver.quit()
    # return links
    #-----------------------------------------------------------
    SOF.Speak("Looking for the best content ...")
    for url in links:
        driver.get(url)
        try:
            # Wait until the page body loads
            WebDriverWait(driver, 10).until(
                # expected Conditions to check for dynamically loaded contents
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Extract paragraph text
            extracted_paragraphs = driver.find_elements(By.TAG_NAME, 'p')
            content = '\n'.join([p.text for p in extracted_paragraphs if p.text.strip()])

            # Alternatively: Try to extract from common article containers
            if not content:
                extracted_divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'article') or contains(@class, 'content')]")
                content = "\n".join([div.text for div in extracted_divs if div.text.strip()])

            if not content:
                content = "Nothing to show ..."
            # get domain name
            domain = extract_domain(url)
            SOF.Speak(f"\n{domain} says\n{content[:500]}\n\n")
            # print(f"\nTelling results from site {domain}\n{content[:500]}...Do you want me to tell more ?\n")
            # sys.exit(0)
            # print(f"\n[{url}] :\n{content[:500]}...\n")
            # return content

        except Exception as e:
            print(f'\033[31mCould not extract content from {url}\nError: {e}\033[0m')
            driver.quit()
            return None
        finally:
            pass
    driver.quit()



while(True):
    query = input("Enter search query : ")
    print(make_google_search(query))


