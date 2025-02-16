from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Function to perform a Google search and extract links
def google_search(query, max_results=5):
    # Set up Selenium Chrome options
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    
    # Set path to ChromeDriver (Update path as needed)
    # service = Service("")  
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome(options=options)

    # Open Google Search
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    driver.get(search_url)

    # Wait for the page to load
    time.sleep(3)  

    # Extract search result links
    results = driver.find_elements(By.XPATH, "//div[@class='tF2Cxc']//a")
    links = [result.get_attribute("href") for result in results[:max_results]]

    # Close the browser
    driver.quit()

    return links

# Example usage
query = input('Enter search query : ')
search_results = google_search(query)

# Print the search results
for i, link in enumerate(search_results, 1):
    print(f"{i}. {link}")
