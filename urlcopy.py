from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip

# 크롬 드라이버 경로 설정 (드라이버가 PATH에 있다면 생략 가능)
chrome_driver_path = 'path/to/chromedriver'

# 브라우저 열기
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# 현재 활성화된 탭의 URL 가져오기
url = driver.current_url
print(f'Current URL: {url}')

# 클립보드에 URL 복사
pyperclip.copy(url)
print('URL has been copied to clipboard.')

# 브라우저 닫기
driver.quit()
