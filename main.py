from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import subprocess
import chromedriver_autoinstaller
import pyperclip
import time

try:
    subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp1"')  # 디버거 크롬 구동
except:
    subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp1"')  # 디버거 크롬 구동
option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install('./')
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
driver.implicitly_wait(20)

print("enter your ID")
id = input()
print("enter your PWD")
pw = input()

# 네이버 로그인
# 1. 네이버 이동
driver.get('https://www.naver.com')

# 2. 로그인 버튼 클릭
elem = driver.find_element_by_class_name('link_login')
elem.click()

# 3. id 복사 붙여넣기
elem_id = driver.find_element_by_id('id')
elem_id.click()
pyperclip.copy(id)
elem_id.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# 4. pw 복사 붙여넣기
elem_pw = driver.find_element_by_id('pw')
elem_pw.click()
pyperclip.copy(pw)
elem_pw.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# 5. 로그인 버튼 클릭
driver.find_element_by_id('log.login').click()

# 6. 이벤트 페이지 이동
driver.get('https://event2.pay.naver.com/event/benefit/list')
