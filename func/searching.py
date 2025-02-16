from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import re
import SpeakOffline as SOF
# Function to perform a Google search and extract links
def make_google_search(query, max_results=5):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Improved headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    # sanitize the query
    query = query.replace('+'," plus ").replace('-'," minus ")
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    driver.get(search_url)
    SOF.Speak(f"Searching internet for {query}")
    time.sleep(3)  # Gives time for search results to load
    # XML Path for complexing matching
    results = driver.find_elements(By.XPATH, "//div[@class='tF2Cxc']//a")
    links = [result.get_attribute("href") for result in results[:max_results]]
    # quit the driver
    driver.quit()
    return links

def extract_domain(url):
    pattern = r"(https?://)?(www\d?\.)?(?P<domain>[\w\.-]+\.\w+)(?:/\S*)?"
    match = re.match(pattern, url)
    if match:
        domain = match.group("domain")
        return domain
    return None

# Extract content from URL
def extract_contents(url):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # Improved headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    SOF.Speak("Looking for the best content ...")
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
        SOF.Speak(f"\nTelling results from {domain}\n{content[:500]}\nDo you want me to tell more ?\n")
        # print(f"\nTelling results from site {domain}\n{content[:500]}...Do you want me to tell more ?\n")
        sys.exit(0)
        # print(f"\n[{url}] :\n{content[:500]}...\n")
        # return content

    except Exception as e:
        print(f'\033[31mCould not extract content from {url}\nError: {e}\033[0m')
        return None
    finally:
        driver.quit()


