# using selenium module
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless=new') # don't show chrome interface to user
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=chrome_options)
website = r'https://ttsmp3.com/text-to-speech/British2English/'


def Speak(*args):
    driver.get(website)
    ButtonSelection = Select(driver.find_element(by=By.ID, value = "sprachwahl"))
    ButtonSelection.select_by_visible_text("US English / Matthew")
    text = "".join(str(i) for i in args).strip()
    
    if not text:
        return
    print(f'\nRete(X) : [\'{text}\b\']\n')
    driver.find_element(By.ID, value = "voicetext").send_keys(text)
    sleep(3)
    driver.find_element(By.ID, value = "vorlesenbutton").click()
    # clear the voicetext area
    sleep(5)
    driver.find_element(By.ID, value = "US English / Matthew").clear()
    sleep(3)
    driver.quit()

query = input('Enter anything : ')
Speak(query)