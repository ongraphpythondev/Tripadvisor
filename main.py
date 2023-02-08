import time
import csv
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from multiprocessing import Process

login_attempt = 0
comment_attempt = 0


def login(driver, email, password):
    try: 
        url = "https://www.tripadvisor.in/"
        driver.get(url)
        time.sleep(2)
        
        WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/header/div/nav/div/div[2]/a[3]'))).click()

        time.sleep(2)
        frame = driver.find_element(By.CSS_SELECTOR, 'body > div.VZmgo.D.X0.X1.Za.Ra > div > div.TocEc._Z.S2.H2._f.WHsPz > div > div > iframe')
        driver.switch_to.frame(frame)

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div[1]/div[3]/div/div[1]/button'))).click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'regSignIn.email'))).send_keys(email)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'regSignIn.password'))).send_keys(password)
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, '#regSignIn > div.coreRegCTAWrapper > button.ui_button.primary.coreRegPrimaryButton.regSubmitBtnEvent').click()
        time.sleep(3)

        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/main/div[3]/div/div/div/form/input[1]'))).send_keys("france")
    
    except:
        global login_attempt
        if login_attempt<5:
            login_attempt += 1
            login(driver, email, password)


def retrive_post(driver):
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#lithium-root > main > div.QvCXh.cyIij.fluiI > div > div > div > form > button.riJbp._G._H.B-._S.t.u.j.Cj.PGlrP"))).click()

    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[2]/span[2]"))).click()
        driver.switch_to.window(driver.window_handles[1])
    except:
        driver.refresh()
        driver.refresh()
        time.sleep(5)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[2]/span[2]"))).click()
        driver.switch_to.window(driver.window_handles[1])

    refresh = False
    try:
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/main/div[7]/div[1]/div[2]/div/div/div[2]/div/ul')))
    except:
        refresh=True

    if refresh:
        driver.refresh()
        time.sleep(5)

    elements = driver.find_element(By.XPATH,"/html/body/div[1]/main/div[7]/div[1]/div[2]/div/div/div[2]/div/ul")
    allLiElement = elements.find_elements(By.TAG_NAME, 'li')
    all_link = []
    for url in allLiElement:
        link_tag = url.find_element(By.TAG_NAME, 'a')
        all_link.append(link_tag.get_attribute('href'))

    return all_link


def post_comment(driver,url,waitingTime):
    try:
        print("Current URL: ",url)
        driver.get(url)
        time.sleep(waitingTime)

        try:
            WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="lithium-root"]/main/div[1]/div[2]/div/div//child::div/button'))).click()
            driver.find_element(By.ID, 'menu-item-3').click()
        except:
            WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="lithium-root"]/main/div[1]/div[2]/div/div//child::div[5]/a'))).click()

        mostViews = {}
        columns = len(driver.find_elements(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div[1]/table/tbody/tr[2]/td'))
        for j in range(2,25):
            if j in (5,9,16):
                continue

            try:
                mostViews[j]=driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div/div[2]/div[1]/table/tbody/tr['+ str(j) +']/td['+ str(columns-1) +']').text
            except:
                print("exception ",j)

        values = list(map(lambda x: int(x.replace(',','')) if ',' in x else int(x), mostViews.values()))
        keys = list(mostViews.keys())
        maxIndex = keys[values.index(max(values))]
        
        question = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div[1]/table/tbody/tr['+ str(maxIndex) +']//child::td/b/a').text
        print(question)
        WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[4]/div[2]/div/div/div[2]/div[1]/table/tbody/tr['+ str(maxIndex) +']//child::td/b/a'))).click()
        print("Clicked")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="message"]'))).send_keys("THis is the my comment")
        time.sleep(5)

    except:
        global comment_attempt
        if comment_attempt <5:
            comment_attempt += 1
            waitingTime+=1
            post_comment(driver,url,waitingTime)


def main(row):    
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.delete_all_cookies()

    email = row[0]
    password = row[1]
    print(email,password)

    login(driver, email, password)
    all_post = retrive_post(driver)
    print(all_post)
    for post in all_post:
        post_comment(driver,post,1)
        break

    print("sucesssss")
    time.sleep(15)
    

if __name__ == "__main__":
    procs = []
    with open('accounts.csv') as f:
        linesObj = csv.reader(f)

        # Instantiating multiple process with arguments
        for row in linesObj:
            proc = Process(target=main, args=(row,))
            procs.append(proc)
            proc.start()

    # Complete the process
    for proc in procs:
        proc.join()
            

