import os
import time
import sda
from selenium import webdriver
from selenium.webdriver.common.by import By
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
                         body="HOTAS available: " + link,
                         from_=os.environ.get('SOURCE_NUM'),
                         to=os.environ.get('TARGET_NUM')
                     )

try:
    while True:
        links = [
            "https://www.bhphotovideo.com/c/product/1433601-REG/logitech_945_000058_g_x56_h_o_t_a_s_rgb.html",
            "https://www.bhphotovideo.com/c/product/1288911-REG/thrustmaster_29607778_t_16000m_fcs_hotas_joystick.html",
            "https://www.bhphotovideo.com/c/product/743173-REG/Thrustmaster_2960720_Hotas_Warthog_Flight_Stick.html"
        ]

        for link in links:
            driver.get(link)
            value = driver.find_element(By.XPATH, "//button[@data-selenium='notifyAvailabilityButton']").text

            if value != "Notify When Available":
                send_msg(link)
                raise StopIteration

        time.sleep(10)
except StopIteration:
    exit()
