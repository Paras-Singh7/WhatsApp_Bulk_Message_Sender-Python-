from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.parse import quote_plus
from sys import platform
import os
from datetime import datetime

options = Options()
if platform == "win32":
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


os.system('colors')
print(f"{bcolors.OKGREEN}")
print("\n")
print("**********************************************************")
print("**********************************************************")
print("*****                                               ******")
print("*****         WhatsApp Bulk Message Sender          ******")
print("*****                                               ******")
print("**********************************************************")
print("**********************************************************")
print(f"{bcolors.ENDC}")


class msg():
    def __init__(self, name):
        self.name = name

    def extract(self):
        global text
        print("Extracting message")
        f = open(self.name, 'r')
        text = f.read()
        f.close()
        print("Done!")

    def display(self):
        print(f"{bcolors.OKCYAN}\nDisplaying message content:  {bcolors.ENDC}")
        print(text)

    def encode(self):
        global text
        text = quote_plus(text)

    def display_encode(self):
        print(f"{bcolors.OKCYAN}\nDisplaying encode message: {bcolors.ENDC}")
        print(text)


msg_filename = input(
    f"{bcolors.OKCYAN}Enter .txt filename that contains message:  {bcolors.ENDC}")
if msg_filename != '':
    msg_filename += '.txt'
else:
    msg_filename = 'message.txt'
message = msg(msg_filename)
message.extract()
message.display()
message.encode()
message.display_encode()

numbers = []


class cntcts:
    def __init__(self, name):
        self.name = name

    def extract(self):
        print("Extracting contacts")
        f = open(cntct_filename, 'r')
        for line in f.read().splitlines():
            if line != "":
                line = "+91" + str(line)
                numbers.append(line)
        f.close()
        print("Done")
        print(
            f"{bcolors.BOLD}{bcolors.HEADER}{len(numbers)} total numbers found{bcolors.ENDC}")


cntct_filename = input(
    f"{bcolors.OKCYAN}\nEnter .txt filename that contains contacts:  {bcolors.ENDC}")
if cntct_filename != '':
    cntct_filename += '.txt'
else:
    cntct_filename = 'numbers.txt'
new = cntcts(cntct_filename)
new.extract()

delay = 30
driver = webdriver.Chrome(ChromeDriverManager().install())
print(f'{bcolors.OKCYAN}Once your browser opens up sign in to web whatsapp{bcolors.ENDC}')
driver.get('https://web.whatsapp.com')
input(f"{bcolors.OKCYAN}Press ENTER after login into Whatsapp Web and your chats are visiable.\n{bcolors.ENDC}")
start_time = datetime.now()
for idx, number in enumerate(numbers):
    number = number.strip()
    if number == "":
        continue
    print(f'{bcolors.OKBLUE}{(idx+1)}/{len(numbers)} => Sending message to {number}.{bcolors.ENDC}')
    try:
        url = 'https://web.whatsapp.com/send?phone=' + \
            number + '&text=' + text + '&app_absent=0'
        sent = False
        for i in range(3):
            if not sent:
                driver.get(url)
                try:
                    click_btn = WebDriverWait(driver, delay).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, '_4sWnG')))
                except Exception as e:
                    print(
                        f"{bcolors.WARNING}Something went wrong..\n Failed to send message to: {number}, retry ({i+1}/3)")
                    print(
                        "Make sure your phone and computer is connected to the internet.")
                    print("If there is an alert, please dismiss it.")
                    input(f"Press enter to continue{bcolors.ENDC}")
                else:
                    sleep(1)
                    click_btn.click()
                    sent = True
                    sleep(2)
                    print(
                        f'{bcolors.BOLD}{bcolors.OKBLUE}Message sent to: {number}\n{bcolors.ENDC}')
    except Exception as e:
        print(
            f'{bcolors.FAIL}Failed to send message to {number} {str(e)} {bcolors.ENDC}')
print(f"{bcolors.FAIL}\nTotal time taken in execution : {datetime.now()-start_time}.{bcolors.ENDC}")
