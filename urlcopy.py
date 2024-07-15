from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip

# webdriver_manager를 사용하여 크롬 드라이버를 자동으로 설치 및 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

while 1:
    copyurlYN = input("현재 url을 복사하겠습니까? y/n : ")
    if(copyurlYN == "y"):
        # 현재 활성화된 탭의 URL 가져오기
        url = driver.current_url
        print(f'Current URL: {url}')

        # 클립보드에 URL 복사
        pyperclip.copy(url)
        print('URL has been copied to clipboard.')

driver.quit()
exit()