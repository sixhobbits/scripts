# scrape the latest operation state from phocos cloud
# 'L' is normal load
# 'B' is battery
# blank is sometimes normal for the most recent state 
# but indicates that no data is being collected if it persists
# we scrape the most recent and second most recent values
# one blank can be ignored, but either 'B' or two blanks in a row 
# is cause for alert.

from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

url = 'https://cloud.phocos.com/d/lB2qKFvMz/phocoslink-cloud?inspect=334&inspectTab=data&orgId=207&from=now-3h&to=now'
browserpath = '/usr/local/bin/chromedriver'
username = ''
password = ''

driverService = Service(browserpath)   
driver = webdriver.Chrome(service=driverService)
driver.get(url)

uf = driver.find_element(By.NAME, "user")
pf = driver.find_element(By.NAME, "password")
uf.send_keys(username)
pf.send_keys(password)

driver.find_element(By.CLASS_NAME,"css-1s0rch-button").click()
driver.implicitly_wait(15) # seconds

xs = driver.find_elements(By.XPATH,"//div[@role = 'cell']")
latest_value = xs[-1].text
latest_ts = xs[-2].text
previous_value = xs[-3].text
previous_ts = xs[-4].text

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

print(d)
