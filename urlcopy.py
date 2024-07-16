from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip
import time
    
if __name__ == "__main__":
    # webdriver_manager를 사용하여 크롬 드라이버를 자동으로 설치 및 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    #임시제어용 변수
    Controler = 1

    while Controler != "exit":
        Controler = input("현재 창의 URL 복사(Y), 종료(exit) ")
        if(Controler == "Y" or Controler == "y" or Controler == "Yes" or Controler == "yes"):

            time.sleep(5)

            # 현재 활성화된 탭의 URL 가져오기
            url = driver.current_url
            print(f'Current URL: {url}')

            # # 클립보드에 URL 복사
            # pyperclip.copy(url)
            # print('URL has been copied to clipboard.')
        if(Controler == "exit"):
            #Chrome 종료
            driver.quit()
            exit()
        