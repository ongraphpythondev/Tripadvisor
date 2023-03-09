from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time


url = "https://pixabay.com/"

driver = webdriver.Chrome()
driver.maximize_window()

driver.get(url)
elems = driver.find_elements(By.CLASS_NAME, "photo-result-image")
print("Total Image In This Page :",len(elems))

for elem in elems:
    print(elem.get_attribute("src"))

WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[1]/div[3]/div[2]/a'))).click()

elems = driver.find_elements(By.CLASS_NAME, "photo-result-image")
print("Total Image In This Page :",len(elems))
for elem in elems:
    img = elem.get_attribute("src")
    if 'jpg' in img:
        print(img)
        img = img.replace('_340.jpg','960_720.jpg')
        print(img)
while True:
    try:
        elems = driver.find_elements(By.CLASS_NAME, "photo-result-image")
        print("Total Image In This Page :",len(elems))
        for elem in elems:
            img = elem.get_attribute("src")
            if 'jpg' in img:
                print(img)
                img = img.replace('_340.jpg','960_720.jpg')
                print(img)
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/a'))).click()
    except:
        break

time.sleep(20)