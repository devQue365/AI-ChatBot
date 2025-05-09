# from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
# options = webdriver.ChromeOptions()
options = uc.ChromeOptions()
options.add_argument("--use-fake-ui-for-media-stream")
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = uc.Chrome(options=options)
url = r"C:\Users\Hp\Desktop\Projects\SAM\AI-ChatBot\func\voice.html"

# get the url
# driver.get(url)
try:
    driver.get(url)
except Exception as e:
    print(f"Error loading page: {e}")

def Listen():
    print("Listening ...")
    driver.find_element(By.ID, value = 'start').click()
    while True:
        output = driver.find_element(By.ID, value = 'output').text
        if output != "":
            print(f"You said : {output}")
            driver.find_element(By.ID, value = 'end').click()
            # driver.service.stop()
            return output

# while True:
#     Listen()