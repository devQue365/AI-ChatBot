import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from requests import get as requests_get
from time import sleep
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# pre defined classes for direct results
classes = set()
classes= {"zCubwf","hgKElc","LTKOO sY7ric","Z0LcW","gsrt vk_bk FzvWSb YwPhnf","pclqee","tw-Data-text tw-text-small tw-ta",
    "IZ6rdc","O5uR6d LTKOO","vlzY6d","webanswers-webanswers_table__webanswers-table",
    "dDoNo ikb4Bb gsrt","sXLaOe","LWkfKe","VQF4g","qv3Wpe","kno-rdesc","SPZz6b",'myclasses',
    "rPeykc","Yh5dPc"
}
new_classes = set(["vk_gy vk_sh card-section sL6Rbf","rPeykc","Yh5dPc","VQF4g","hgKElc","kno-rdesc","YpjmDb LLotyc","vk_bk dDoNo FzvWSb","Ww4FFb vt6azd","z7BZJb XSNERd","QoPDcf CYJS5e","Ab33Nc"
])
classes = classes.union(new_classes)

def genEffect(arg)->str|None:
    arg = str(arg).split(' ')
    for i in arg:
        print(i,end=" ")
        sleep(0.07)
    print()




def initialize_driver():
    # Initialize the Chrome options
    options = uc.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    # if(headless):
        # options.add_argument("--headless=new")  # For Chrome 109+, improves detection avoidance
    options.add_argument("--disable-gpu")  # Required for headless mode on some systems
    options.add_argument("--log-level=3")  # Required for headless mode on some systems
    options.add_argument("--window-size=1920,1080")  # Set window size to avoid detection
    options.add_argument("--no-sandbox")  # Bypasses OS security model
    options.add_argument("--disable-dev-shm-usage")  # Helps with performance in containers
    options.add_argument("--disable-blink-features=AutomationControlled")  # Makes Selenium harder to detect
    options.add_argument("--disable-background-timer-throttling")  # No delay on timers
    options.add_argument("--disable-backgrounding-occluded-windows")  # Keeps execution fast
    options.add_argument("--disable-renderer-backgrounding")  # No render delay
    options.add_argument("--blink-settings=imagesEnabled=false")  # Disables images
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
    ''' If user searches for weather or temperature '''
    if ('weather' in query) or ('temperature' in query):
        try:
            # Extract temperature
            temperature = driver.find_element(By.XPATH, '//span[@id="wob_tm"]').text
            unit = driver.find_element(By.XPATH, '//div[@id="wob_dts"]').text

            # Extract weather condition
            condition = driver.find_element(By.XPATH, '//span[@id="wob_dc"]').text

            return f"Temperature: {temperature}°C, Weather: {condition} ({unit})"
        
        except Exception as e:
            return f"Error: {e}"
    # Look for common classes for direct results
    result = None
    for class_name in classes:
        try:
            element = driver.find_element(By.CLASS_NAME, class_name)
            extracted_text = element.text.strip()

            if extracted_text:
                print(f"Found at \033[32m{class_name}\033[0m")  # Debugging
                result = extracted_text  # Store the result but do not break
                driver.quit()
                return result
        except Exception as e:
            print(f"Error finding class {class_name}: {e}")
    ''' Search websites for results '''
    genEffect("\033[34m\033[1mSearching websites for the best results ...\033[0m")
    results = driver.find_elements(By.XPATH, "//div[@class='tF2Cxc']//a")
    links = [result.get_attribute("href") for result in results[:max_results]]
    for url in links:
        driver.get(url)
        try:
            # Wait until the page body loads
            WebDriverWait(driver, 10).until(
                # expected Conditions to check for dynamically loaded contents
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            domain = extract_domain(url)
            result = f"{domain} says\n"
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
            # domain = extract_domain(url)
            # genEffect(f"\033[34m\n{domain} says\n")#{content[:500]}\n\n\033[0m")
            # SOF.Speak(f"\n{domain} says\n{content[:500]}\n\n")
            # print(f"\nTelling results from site {domain}\n{content[:500]}...Do you want me to tell more ?\n")
            # sys.exit(0)
            # print(f"\n[{url}] :\n{content[:500]}...\n")
            # return content
            result += content
            driver.quit()
            return result

        except Exception as e:
            content = f'\033[31mCould not extract content from {url}\nError: {e}\033[0m'
            result += content
            driver.quit()
            return result
# while(True):
#     result = search_google(input('Enter your query : '))
#     # Print the result to verify it works
#     if(result):
#         genEffect(f'The result we got:\n{result}')
#     else:
#         genEffect("\033[1m\033[31mSorry, I ran into problem :(\033[0m")
# genEffect("Lorem ipsum dolor sit amet consectetur adipisicing elit. Corrupti, consequuntur similique. Rem beatae aliquid, eum praesentium soluta labore impedit! Asperiores perspiciatis eaque, excepturi deleniti corporis repudiandae expedita impedit dolorum cupiditate.")