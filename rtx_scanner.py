import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from twilio.rest import Client

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--log-level=3")
chrome_options.binary_location = GOOGLE_CHROME_PATH
driver = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, options=chrome_options)


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
        driver.get("https://www.newegg.com/p/pl?d=rtx+3080")

        titles = driver.find_elements_by_class_name("item-title")
        elements = driver.find_elements_by_class_name("item-promo")

        item = 0
        links = {}

        for title in titles:
            if "3080" in title.text:
                links[item] = title.get_attribute("href")
                item += 1

        item = 0
        for element in elements:
            if element.text == "OUT OF STOCK":
                send_msg(links[item])
                raise StopIteration
            item += 1

        time.sleep(10)
except StopIteration:
    exit()