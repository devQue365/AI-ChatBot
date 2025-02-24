import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from requests import get as requests_get
from time import sleep
import re

# Predefined Google direct answer classes
direct_answer_classes = {
    "Z0LcW", "hgKElc", "LTKOO sY7ric", "gsrt vk_bk FzvWSb YwPhnf",
    "dDoNo ikb4Bb gsrt", "sXLaOe", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc"
}

def initialize_driver():
    options = uc.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")  
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    return driver

def check_connection(url):
    try:
        response = requests_get(url, timeout=5)
        return True
    except requests.exceptions.RequestException:
        return False

def search_google(query, max_results=5):
    if not check_connection('https://www.google.com'):
        return "Please check your internet connection ..."

    driver = initialize_driver()
    
    query = query.replace('+', ' plus ').replace('-', ' minus ')
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    driver.get(url)
    
    sleep(3)  # Allow page to load

    # Try to extract direct answer from Google
    for class_name in direct_answer_classes:
        try:
            element = driver.find_element(By.CLASS_NAME, class_name)
            result = element.text.strip()
            if result:
                print(f"Direct answer found at \033[32m{class_name}\033[0m")  
                driver.quit()
                return result
        except:
            pass

    # Extract normal search results (titles, links, descriptions)
    search_results = []
    try:
        results = driver.find_elements(By.XPATH, '//div[@class="tF2Cxc"]')[:max_results]
        for result in results:
            try:
                title = result.find_element(By.TAG_NAME, "h3").text
                link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                description = result.find_element(By.CLASS_NAME, "VwiC3b").text
                search_results.append(f"Title: {title}\nURL: {link}\nDescription: {description}\n")
            except:
                continue
    except:
        pass

    driver.quit()
    
    return "\n\n".join(search_results) if search_results else "No search results found."

while True:
    query = input("Enter your query: ")
    result = search_google(query)
    
    if result:
        print(f"\n\033[1mSearch Results:\033[0m\n{result}")
    else:
        print("\033[1m\033[31mSorry, I ran into a problem :(\033[0m")
