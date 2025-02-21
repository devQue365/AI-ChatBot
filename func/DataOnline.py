import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from requests import get as requests_get
from time import sleep
import re

# pre defined classes for direct results
classes = set()
classes= {"zCubwf","hgKElc","LTKOO sY7ric","Z0LcW","gsrt vk_bk FzvWSb YwPhnf","pclqee","tw-Data-text tw-text-small tw-ta",
    "IZ6rdc","O5uR6d LTKOO","vlzY6d","webanswers-webanswers_table__webanswers-table",
    "dDoNo ikb4Bb gsrt","sXLaOe","LWkfKe","VQF4g","qv3Wpe","kno-rdesc","SPZz6b",'myclasses',
    "rPeykc","Yh5dPc"
}
new_classes = set(["vk_gy vk_sh card-section sL6Rbf","rPeykc","Yh5dPc","VQF4g","hgKElc","kno-rdesc","YpjmDb LLotyc","vk_bk dDoNo FzvWSb","Ww4FFb vt6azd","z7BZJb XSNERd","QoPDcf CYJS5e"
])
classes = classes.union(new_classes)

def initialize_driver():
    # Initialize the Chrome options
    options = uc.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    # if(headless):
        # options.add_argument("--headless=new")  # For Chrome 109+, improves detection avoidance
    options.add_argument("--disable-gpu")  # Required for headless mode on some systems
    options.add_argument("--window-size=1920,1080")  # Set window size to avoid detection
    options.add_argument("--no-sandbox")  # Bypasses OS security model
    options.add_argument("--disable-dev-shm-usage")  # Helps with performance in containers
    options.add_argument("--disable-blink-features=AutomationControlled")  # Makes Selenium harder to detect
    # Launch Chrome with undetected_chromedriver
    driver = uc.Chrome(options=options)
    return driver

def search_google(query, max_results=2):
    # nested function to extract domain name
    def extract_domain(url):
        pattern = r"(https?://)?(www\d?\.)?(?P<domain>[\w\.-]+\.\w+)(?:/\S*)?"
        match = re.match(pattern, url)
        if match:
            domain = match.group("domain")
            return domain
        return None
    # nested function to check network connection
    def check_connection(url):
        try:
            response = requests_get(url, timeout=5)
            return True
        except ConnectionError:
            return False
    # check for internet connection
    if not check_connection('https://www.google.com'):
        return "Please check your internet connection ..."
    driver = initialize_driver()

    # sanitize the query
    query = query.replace('+',' plus ').replace('-',' minus ')
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    driver.get(url)
    sleep(5) # waiting time for pages to load
    # Look for common classes for direct results
    for class_name in classes:
        try:
            element = driver.find_element(By.CLASS_NAME, class_name)
            result = element.text.strip()
            if result:
                print(f"Found at \033[32m{class_name}\033[0m") # To check for the google class
                driver.quit()
                return result
        except:
            pass
    driver.quit()
while(True):
    result = search_google(input('Enter your query : '))
    # Print the result to verify it works
    if(result):
        print(f'The result we got:\n{result}')
    else:
        print("\033[1m\033[31mSorry, I ran into problem :(\033[0m")
