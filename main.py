from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import subprocess
import chromedriver_autoinstaller
import pyperclip
import pyautogui as pag
import pywinauto
import pygetwindow as gw
import time

def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

"""
chromedriver.exe를 사용해서 작동 수행해야하므로 현재 버전에 맞는 chromedriver.exe 자동으로 받게끔 함
또한 debuggeraddress를 사용해서 테스트 모드 아닌 일반 크롬창에서의 동작 수행
"""
try:
    # 디버거 크롬 구동
    subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp1"')
except:
    # 디버거 크롬 구동
    subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp1"')
option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install('./')
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
driver.implicitly_wait(20)

# 콘솔 입력
print("enter your ID")
id = input()
print("enter your PWD")
pw = input()


driver.get('https://www.naver.com')

# 로그인 버튼 클릭
elem = driver.find_element(By.XPATH, '//*[@id="account"]/a')
elem.click()

# ID 복사 붙여넣기
elem_id = driver.find_element(By.ID, 'id')
elem_id.click()
pyperclip.copy(id)
elem_id.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# PW 복사 붙여넣기
elem_pw = driver.find_element(By.ID, 'pw')
elem_pw.click()
pyperclip.copy(pw)
elem_pw.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# 로그인 버튼 클릭
driver.find_element(By.ID, 'log.login').click()

# 이벤트 페이지 이동
driver.get('https://event2.pay.naver.com/event/benefit/list')

# 클릭적립은 container 최상위 표시되는 li에 있으므로 for문으로 전부 클릭
for i in range(1, 16):
    driver.find_element(By.XPATH, '//*[@id="eventList"]/li['+str(i)+']/a').click()
    time.sleep(2)
    try:
        # driver.switch_to.alert() 안먹힘... 따라서 pyautogui로 엔터를 입력해서 팝업을 닫아버린다
        # 당연히 엔터키로 팝업을 닫으니까 크롬에 포커스 줘서 크롬 프로세스에서 엔터를 입력받을 수 있게 함
        focus_chrome = gw.getWindowsWithTitle('Chrome')[0]
        if focus_chrome.isActive == False:
            pywinauto.application.Application().connect(handle=focus_chrome._hWnd).top_window().set_focus()
        pag.press('ENTER')
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[0])
    except:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[0])

# 매일 리셋되는 적립

driver.get('https://ofw.adison.co/u/naverpay/ads/89582')
driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div/div/button').click()
time.sleep(2)

driver.get('https://ofw.adison.co/u/naverpay/ads/89601')
driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/div/div/button').click()
time.sleep(2)

driver.quit()
print("폐지 다 주웠습니다 주인님...")