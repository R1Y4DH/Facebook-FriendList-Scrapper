from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import math #temp

email = input("Your email: ")
pwd = input("Your password: ")
wait = 2

options = Options()

options.add_argument("--disable-infobars")
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")
# options.add_argument("--headless")

# Pass the argument 1 to allow and 2 to block
options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 2}
)

PATH = "chromedriver.exe"
driver = webdriver.Chrome("/usr/bin/chromedriver",
                            chrome_options=options)

driver = webdriver.Chrome(
    chrome_options=options, executable_path=PATH
)
driver.get("https://www.facebook.com/")
user_name = driver.find_element(By.XPATH,"//input[@type='text']")
print("inputting email")
user_name.send_keys(email)

password = driver.find_element(By.XPATH,"//input[@placeholder='Password']")
print("inputting password")
password.send_keys(pwd)

log_in_button = driver.find_element(By.XPATH,"//button[@type='submit']")
print("submit")
log_in_button.click()
print("if you have verification code please input them and continue, otherwise ignore this message")

WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH,"//*[name()='svg' and @aria-label='Your profile']")))
profile = driver.find_element(By.XPATH,"//*[name()='svg' and @aria-label='Your profile']")
print("navigating to profile")
profile.click()
WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH,"//a[@href='/me/']")))
my_profile = driver.find_element(By.XPATH,"//a[@href='/me/']")
my_profile.click()
sleep(wait)

totalfriends = 0
userFriends = driver.find_elements(By.XPATH,"//a[text()=' friends']")
number, text = userFriends[0].text.split(" ")
# totalfriends = int(number)
acttotalfriends = int(number)
totalfriends = math.trunc(int(number)/2)

print(acttotalfriends,"friends found but due to limitation",totalfriends,"will be extract")

if totalfriends != 0:

    friendsTab = driver.find_element(By.XPATH,"//div[span[text()='Friends']]")
    print("navigating to friends")
    friendsTab.click()
    sleep(wait)

    friendsList = []
    friend = []

    my_friend = driver.find_elements(By.XPATH,"//div[@class='x1iyjqo2 x1pi30zi']")
    print("scrolling & extracting...")
    while True:
        for friend in my_friend:
            friendsList.append(friend.text)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(wait)
        my_friend = driver.find_elements(By.XPATH,"//div[@class='x1iyjqo2 x1pi30zi']")
        if len(set(friendsList)) > totalfriends:
            break
            
    clsFriends = list(dict.fromkeys(friendsList))            

    print("total of",len(clsFriends),"extracted")

    driver.quit()

    for friends in clsFriends:
        if friends.count("\n") > 2:
            pass
        elif friends.find("\n") != -1:
            name, txt1 = friends.split("\n")
            friend = [name]
        else:
            friend = [name]

    print("operation complete")
else:
    print("operation canceled")