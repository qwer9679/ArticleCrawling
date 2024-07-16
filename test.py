from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import trafilatura
import pyperclip
import time
import re

def savetxt(Title : str, MainPost : str):
    """
    기사의 본문, 제목을 txt파일로 저장합니다.\n
    Title : 기사의 제목을 파일의 이름으로 저장합니다.\n
    MainPost : 기사의 내용을 txt 파일에 저장합니다.
    """
    file_path = Title + ".txt"

    # 파일을 쓰기 모드로 열고 문자열을 파일에 작성합니다.
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(MainPost)

    print(f"기사내용이 {file_path}파일에 저장되었습니다.")
    
def IncheonTitle(originpost : str, PostNumber : int):
    """
    경기도교육청 보도자료에서 크롤링된 내용 중\n
    제목을 가져오는 함수입니다.
    """

    mainPost = originpost

    if mainPost:
        prepost = ".*" + str(PostNumber) + ". "
        pospost = str(PostNumber + 1) + ". " + ".*"
        #제목 이전 불필요한 텍스트 제거
        mainPost = re.sub(prepost, '', originpost, flags=re.DOTALL)
        mainPost = re.sub(pospost,'', originpost, flags=re.DOTALL)

        #제목 이후 불필요한 텍스트 제거
        return mainPost
    else:
        print("잘못된 url입니다.")

if __name__ == "__main__":
    option = Options()
    # webdriver_manager를 사용하여 크롬 드라이버를 자동으로 설치 및 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=option)
    #임시제어용 변수
    Controler = 1

    while Controler != "exit":
        Controler = input("현재 창의 URL 복사(Y), 종료(exit) ")
        if(Controler == "Y" or Controler == "y" or Controler == "Yes" or Controler == "yes"):
            print("추출중입니다...")
            time.sleep(5)

            # 현재 활성화된 탭의 URL 가져오기
            url = driver.current_url
            page_source = trafilatura.extract(driver.page_source)
            subpost = []
            for i in range(10):
                subpost[i] = IncheonTitle(page_source, i)
                savetxt("test" + str([i]) + ".txt", subpost[i])

        if(Controler == "exit"):
            #Chrome 종료
            driver.quit()
            exit()