import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

URL = 'https://cloud.phocos.com/d/lB2qKFvMz/phocoslink-cloud?orgId=207&refresh=5m&inspect=353&inspectTab=data'
USERNAME = ''
PASSWORD = ''
DRIVER_PATH = '/usr/bin/chromedriver'
BROWSER_PATH = '/usr/bin/google-chrome'

def get_latest_status():

    options = Options()
    options.binary_location = BROWSER_PATH
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    options.add_argument('--window-size=1920,1080')

    url = URL
    browserpath = DRIVER_PATH
    username = USERNAME
    password = PASSWORD

    driverService = Service(browserpath)
    driver = webdriver.Chrome(options=options, service=driverService)
    driver.get(url)

    uf = driver.find_element(By.NAME, "user")
    pf = driver.find_element(By.NAME, "password")
    uf.send_keys(username)
    pf.send_keys(password)

    driver.get(url)

    uf = driver.find_element(By.NAME, "user")
    pf = driver.find_element(By.NAME, "password")
    uf.send_keys(username)
    pf.send_keys(password)

    # click login button
    driver.find_element(By.CLASS_NAME,"css-12ciaym-button").click()
    driver.implicitly_wait(5)
    footer = driver.find_element(By.TAG_NAME, 'footer')
    driver.execute_script("arguments[0].scrollIntoView();", footer)

    # click download CSV button
    # driver.find_element(By.CLASS_NAME,"css-ti38pk-button").click()

    # click sort by Time button
    driver.find_element(By.CLASS_NAME, "css-1xdjzer").click()
    # driver.implicitly_wait(1)
    driver.find_element(By.CLASS_NAME, "css-1xdjzer").click()


    xs = driver.find_elements(By.XPATH, "//div[@role = 'cell']")
    latest_value = xs[1].text
    latest_ts = xs[0].text
    previous_value = xs[3].text
    previous_ts = xs[2].text

    d = {
        "latest": {
            "ts": latest_ts,
            "value": latest_value
        },
        "previous": {
            "ts": previous_ts,
            "value": previous_value
        }
    }

    return d
