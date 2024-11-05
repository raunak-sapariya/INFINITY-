from selenium.webdriver.chrome.options import Options 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
 


def generateQuestion(para):

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    

    url="https://www.huggingface.co"

    cookies=[{'domain': '.huggingface.co', 'expiry': 1731350349, 'httpOnly': False, 'name': '_ga', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.2.544560895.1696790327'}, {'domain': '.huggingface.co', 'expiry': 1731350349, 'httpOnly': False, 'name': '_ga_8Q63TH4CSL', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GS1.1.1696790326.1.1.1696790349.37.0.0'}, {'domain': '.huggingface.co', 'expiry': 1696792150, 'httpOnly': False, 'name': '__stripe_sid', 'path': '/', 'sameSite': 'Strict', 'secure': True, 'value': 'fe53ba60-5426-45d4-b0c1-71c7889bf912bf3d0b'}, {'domain': '.huggingface.co', 'expiry': 1728326350, 'httpOnly': False, 'name': '__stripe_mid', 'path': '/', 'sameSite': 'Strict', 'secure': True, 'value': '309c171d-458c-4e75-aed0-35090b179d698aa13e'}, {'domain': '.huggingface.co', 'expiry': 1696790386, 'httpOnly': False, 'name': '_gat', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1'}, {'domain': '.huggingface.co', 'expiry': 1728326349, 'httpOnly': True, 'name': 'token', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'VHDmxxIJAbxLLIvaXkkFlCoezicBqcASeSkbAFQtPGOhCffQvJWeMrrlrfplZNUKXIyKMuehZsgzAjWZokqfIRDxkLtqDatMaSnBZJsWPbehcAujnmMESOJEhEDeeBZl'}, {'domain': '.huggingface.co', 'expiry': 1696876749, 'httpOnly': False, 'name': '_gid', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'GA1.2.994350151.1696790327'}] 


    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    for i in range(len(cookies)):
        driver.add_cookie(cookies[i])
    driver.refresh()

    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.RETURN).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.RETURN).perform()

    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.TAB).perform()
    actions.send_keys(Keys.RETURN).perform()

    form=driver.find_elements(By.TAG_NAME,"form")[1]
    form.find_element(By.TAG_NAME,"button").click()
    
  

    textArea = driver.find_element(By.CSS_SELECTOR, f'textarea[placeholder="Ask anything"]')
    textArea.click()
    textArea.send_keys('''Generate one array python of 2 multiple-choice questions in strict JSON format of {question:"question related to topic,options:one array of multile options to choose from,answer:"Correct answer" '} related to the following summary: '''+ para)

    send=driver.find_elements(By.CLASS_NAME,"btn")[1].click()
    time.sleep(15)


    data=""
    try:

        data=driver.find_element(By.TAG_NAME,"code").text
    except:
        element=driver.find_element(By.CLASS_NAME,"prose")
        data=element.find_element(By.TAG_NAME,"p").text
    driver.quit()    
    try:
       
        return json.loads(data)  
    except :
        return None


    
