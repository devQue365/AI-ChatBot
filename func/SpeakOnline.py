# using selenium module
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # don't show chrome interface to user
chrome_options.headless = True

driver = webdriver.Chrome(options=chrome_options)
website = r'https://ttsmp3.com/text-to-speech/British2English/'
driver.get(website)

ButtonSelection = Select(driver.find_element(by=By.ID, value = "sprachwahl"))
ButtonSelection.select_by_visible_text("British English / Brian")

def Speak(*args):
    text = ""
    for i in args:
        text+= (str(i)  + ' ')
    
    lengthOfText = len(str(text))
    if(lengthOfText == 0):
        pass
    else:
        print(f'\nRete(X) : [\'{text}\b\']\n')
        push_data = str(text)
        driver.find_element(By.ID, value = "voicetext").send_keys(push_data)
        driver.find_element(By.ID, value = "vorlesenbutton").click()
        # clear the voicetext area
        driver.find_element(By.ID, value = "voicetext").clear()

query = input('Enter anything : ')
Speak(query)