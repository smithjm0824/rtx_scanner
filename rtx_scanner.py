import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from twilio.rest import Client

CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
chrome_bin = os.environ.get("GOOGLE_CHROME_BIN", "chromedriver")
options = webdriver.ChromeOptions()
options.binary_location = chrome_bin
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--headless")
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)


def send_msg(link):
    account_sid = os.environ.get('ACCT_ID')
    auth_token = os.environ.get('AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body="RTX 3080 available: " + link,
                         from_=os.environ.get('SOURCE_NUM'),
                         to=os.environ.get('TARGET_NUM')
                     )

try:
    while True:
        driver.get("https://www.newegg.com/p/pl?d=RTX+30&N=50001402%2050001314%2050001312%2050001315")

        titles = driver.find_elements_by_class_name("item-title")
        elements = driver.find_elements_by_class_name("item-promo")

        item = 0
        links = {}

        for title in titles:
            links[item] = title.get_attribute("href")
            item += 1

        item = 0
        for element in elements:
            if element.text != "OUT OF STOCK":
                send_msg(links[item])
                raise StopIteration
            item += 1

        time.sleep(10)
except StopIteration:
    exit()