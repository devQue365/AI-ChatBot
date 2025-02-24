from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--use-fake-ui-for-media-stream")
# options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
url = r"C:\Users\Hp\Desktop\Projects\projX\projX\data\voice.html"

# get the url
driver.get(url)

def Listen():
    print("Listening ...")
    driver.find_element(By.ID, value = 'start').click()
    while True:
        output = driver.find_element(By.ID, value = 'output')
        if output.text != "":
            print(f"You said : {output.text}")
            driver.find_element(By.ID, value = 'end').click()
            return output

while True:
    Listen()

