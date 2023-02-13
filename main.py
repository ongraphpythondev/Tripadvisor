import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from multiprocessing import Process
from openapi import chatResponse

login_attempt = 0
comment_attempt = 0
location_attempt = 0
element_attempt = 0

options = Options()
# options.add_argument("--headless")

def login(driver, email, password):
    global login_attempt
    if login_attempt>0:
        time.sleep(5)
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

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/main/div[3]/div/div/div/form/input[1]'))).send_keys("france")
    
    except:
        if login_attempt<6:
            driver.delete_all_cookies()
            login_attempt += 1
            print(f"Login Attempt +++++++++++++++++++++++++++++++++  :{login_attempt}")
            login(driver, email, password)
        else:
            print("Login exit &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            driver.quit()
            exit()

def click_locations(driver):
    global location_attempt
    if location_attempt>0:
        time.sleep(5)
    try:
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div/div/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[2]/span[2]"))).click()
        driver.switch_to.window(driver.window_handles[1])
    except:
        
        if location_attempt<5:
            driver.refresh()
            location_attempt+=1
            print(f"click_location $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ :{location_attempt}")
            click_locations(driver)
        else:
            print("Click location exit ********************************")
            driver.quit()
            exit()


def get_element_selector(driver):
    global element_attempt
    if element_attempt>0:
        driver.refresh()
        time.sleep(10)
    try:
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/main/div[7]/div[1]/div[2]/div/div/div[2]/div/ul')))
        elements = driver.find_element(By.XPATH,"/html/body/div[1]/main/div[7]/div[1]/div[2]/div/div/div[2]/div/ul")
        return elements
    except:
        if element_attempt<6:
            driver.refresh()
            element_attempt +=1
            print(f"element_attempt ############################ :{element_attempt}")
            return get_element_selector(driver)
        else:
            print("Element exit ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            driver.quit()
            exit()



def retrive_post(driver):
    try:
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#lithium-root > main > div.QvCXh.cyIij.fluiI > div > div > div > form > button.riJbp._G._H.B-._S.t.u.j.Cj.PGlrP"))).click()
    except:
        print("Here it is ============================")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/main/div[3]/div/div/div/form/input[1]'))).send_keys("france")
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#lithium-root > main > div.QvCXh.cyIij.fluiI > div > div > div > form > button.riJbp._G._H.B-._S.t.u.j.Cj.PGlrP"))).click()
    
    click_locations(driver)
    elements = get_element_selector(driver)
    if not elements:
        driver.quit()
        exit()    

    allLiElement = elements.find_elements(By.TAG_NAME, 'li')
    all_link = []
    for url in allLiElement:
        link_tag = url.find_element(By.TAG_NAME, 'a')
        all_link.append(link_tag.get_attribute('href'))

    return all_link


def post_comment(driver,url,waitingTime):
    global comment_attempt
    if comment_attempt>0:
        time.sleep(5)
    try:
        print("Current URL: ",url)
        driver.get(url)
        time.sleep(waitingTime)
        # print("searching for country location")
        # country = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#lithium-root > main > div.cBOoN > div.QvCXh.mvTrV.cyIij.fluiI > div > h1 > span > span.\{geoClass\}'))).text
        # # country = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[1]/div[1]/div/h1/span/span[2]').text
        # print(f"countey location is : {country}")

        try:
            WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="lithium-root"]/main/div[1]/div[2]/div/div//child::div/button'))).click()
            time.sleep(1)
            driver.find_element(By.ID, 'menu-item-3').click()
        except:
            WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="lithium-root"]/main/div[1]/div[2]/div/div//child::div[5]/a'))).click()

        mostViews = {}
        columns = len(driver.find_elements(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div[1]/table/tbody/tr[2]/td'))
        print(f"Columns {columns}")
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

        # question = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div/div[2]/div[1]/table/tbody/tr['+ str(maxIndex) +']//child::td/b/a').text
        # print(f"The question is : {question}")
        WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[4]/div[2]/div/div/div[2]/div[1]/table/tbody/tr['+ str(maxIndex) +']//child::td/b/a'))).click()
        print("Clicked")
        mainquestion = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div[2]/div/div[2]/div[1]/div[5]/div/div/div[2]/div[1]/div[2]'))).text
        mainquestion = f'"{mainquestion}"'+' generate a reply for advertisement and advantage of "travpart" app'
        print(mainquestion)
        response = chatResponse(mainquestion)
        if response[:2]=="AI":
            response = response[3:]
        print(response)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="message"]'))).send_keys(response)
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'submitButton'))).click()
        time.sleep(5)

    except:
        if comment_attempt <10:
            comment_attempt += 1
            waitingTime+=1
            print(f"comment Attempt ---------------------------  :{comment_attempt}")
            post_comment(driver,url,waitingTime)
        else:
            print("comment exit @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            driver.quit()
            exit()

def main(row):    
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.delete_all_cookies()

    email = row[0]
    password = row[1]
    print(email,password)

    login(driver, email, password)
    all_post = retrive_post(driver)
    print(all_post)
    for post in all_post[1:]:
        post_comment(driver,post,1)
        # break

    print("sucesssss")
    driver.quit()
    

# if __name__ == "__main__":
#     procs = []
#     with open('accounts.csv') as f:
#         linesObj = csv.reader(f)

#         # Instantiating multiple process with arguments
#         for row in linesObj:
#             proc = Process(target=main, args=(row,))
#             procs.append(proc)
#             proc.start()

#     # Complete the process
#     for proc in procs:
#         proc.join()
            

