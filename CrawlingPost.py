import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import trafilatura.settings
from trafilatura.settings import use_config
import trafilatura
import re

config = use_config()

config.set('DEFAULT', 'max_redirects', '10')
config.set('DEFAULT', 'download_timeout', '30')
config.set('DEFAULT', 'max_file_size', '20000000')
config.set('DEFAULT', 'min_file_size', '10')
config.set('DEFAULT', 'sleep_time', '5')
config.set('DEFAULT', 'user_agents', '5')
config.set('DEFAULT', 'cookie', '')
config.set('DEFAULT', 'min_extracted_size', '250')
config.set('DEFAULT', 'min_extracted_comm_size', '1')
config.set('DEFAULT', 'min_output_size', '1')
config.set('DEFAULT', 'min_output_comm_size', '1')
config.set('DEFAULT', 'extraction_timeout', '30')
config.set('DEFAULT', 'min_duplcheck_size', '100')
config.set('DEFAULT', 'max_repetitions', '2')
config.set('DEFAULT', 'extensive_date_search', 'on')
config.set('DEFAULT', 'external_urls', 'off')
class Chromeapp:
    def __init__(self, root):
        """
        GUI 구현
        """
        try:
            self.root = root
            self.driver = None
            # OpenChrome()
            self.root.geometry("600x400")
            self.root.title("CrawlingPost")
            self.root.resizable(False, False)

            self.root.grid_rowconfigure(0, minsize=100)
            self.root.grid_rowconfigure(1, weight=1)
            self.root.grid_rowconfigure(2, weight=2)

            self.root.grid_columnconfigure(0, minsize=100)
            self.root.grid_columnconfigure(1, weight=1)
            self.root.grid_columnconfigure(2, weight=1)
            self.root.grid_columnconfigure(3, weight=1)

            self.Incheon = tk.Button(root, text="인천", command=self.OpenIncheon)
            self.Incheon.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

            self.Seoul = tk.Button(root, text="서울", command=self.OpenSeoul)
            self.Seoul.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

            self.Geonggido = tk.Button(root, text="경기", command=self.OpenGeonggido)
            self.Geonggido.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

            CopyPost = tk.Button(root, text="크롬 기사 복사", command=self.CrawlingPost)
            CopyPost.grid(row=0, column=3, sticky="nsew", padx=10, pady=10)

            self.exeTitle = tk.Text(root, height=2, width=50)
            self.exeTitle.grid(row=1,column = 0, columnspan = 3, sticky="nsew", padx=10, pady=10)

            TitleCopy = tk.Button(root, text="제목 복사", command=self.CopyTitle)
            TitleCopy.grid(row=1, column=3, sticky="nsew", padx=10, pady=10)

            self.exePost = tk.Text(root, height=16, width=40)
            self.exePost.grid(row=2,column = 0, columnspan = 3, sticky="nsew", padx=10, pady=10)

            PostScroll = tk.Scrollbar(root, orient="vertical", command=self.exePost.yview)
            PostScroll.grid(row=2,column=2,columnspan=3, sticky="ns")

            self.exePost.config(yscrollcommand=PostScroll.set)

            PostCopy = tk.Button(root, text="내용 복사", command=self.CopyPost)
            PostCopy.grid(row=2, column=3, sticky="nsew", padx=10, pady=10)

            self.root.mainloop()
        except Exception as e:
            print(f"exe에서 오류 발생 : {e}")

    def OpenGeonggido(self):
        #webdriver_manager를 이용해 크롬 드라이버를 자동 설치/업데이트 후 실행
        try:
            if self.driver is None:

                option = Options()
                option.add_experimental_option("detach", True)
                service = Service()
                self.driver = webdriver.Chrome(service=service, options=option)
            url = f"https://www.goe.go.kr/home/bbs/bbsList.do?menuId=100000000000059&bbsMasterId=BBSMSTR_000000000163&menuInit=2,2,0,0,0&searchCategory=%EB%8F%84%EA%B5%90%EC%9C%A1%EC%B2%AD"
            self.driver.get(url)
        except Exception as e:
            print(f"OpenGeonggido에서 오류 발생 : {e}")

    def OpenSeoul(self):
        #webdriver_manager를 이용해 크롬 드라이버를 자동 설치/업데이트 후 실행
        try:
            if self.driver is None:
                option = Options()
                option.add_experimental_option("detach", True)
                service = Service()
                self.driver = webdriver.Chrome(service=service, options=option)
            url = f"https://enews.sen.go.kr/news/list.do?step1=3&step2=1"
            self.driver.get(url)
        except Exception as e:
            print(f"OpenSeoul에서 오류 발생 : {e}")

    def OpenIncheon(self):
        #webdriver_manager를 이용해 크롬 드라이버를 자동 설치/업데이트 후 실행
        try:
            if self.driver is None:
                option = Options()
                option.add_experimental_option("detach", True)
                service = Service()
                self.driver = webdriver.Chrome(service=service, options=option)
            url = f"https://www.ice.go.kr/ice/na/ntt/selectNttList.do?mi=11620&bbsId=1519"
            self.driver.get(url)
        except Exception as e:
            print(f"OpenIncheon에서 오류 발생 : {e}")

    def CrawlingPost(self):
        # try:
            if self.driver:
                current_url = self.driver.current_url
                if(self.contain_char(current_url, "www.goe.go.kr")):
                    print("경기도 기사 크롤링 시작")
                    Title = self.GyeonggidoTitle(current_url)
                    if Title is not None:
                        print("경기도 기사 제목 크롤링 성공")
                    Post = self.GyeonggidoPost(current_url)
                    Post = re.sub(re.escape(Title), '', Post)
                    if Post is not None:
                        print("경기도 기사 내용 크롤링 성공")

                elif(self.contain_char(current_url, "enews.sen.go.kr")):
                    print("서울 기사 크롤링 시작")
                    Title = self.SeoulTitle(current_url)
                    if Title is not None:
                        print("서울 기사 제목 크롤링 성공")

                    Post = self.SeoulPost(current_url)
                    if Post is not None:
                        print("서울 기사 내용 크롤링 성공")

                elif(self.contain_char(current_url, "www.ice.go.kr")):
                    page_source = trafilatura.extract(self.driver.page_source, config=config)
                    
                    #기사 수 체크
                    pattern = r'<meta property="og:title" content="(.*?)">'
                    postnumber = re.search(pattern, self.driver.page_source)
                    pattern = r'.* 외 '
                    PostCount = re.sub(pattern, '', postnumber.group(1))
                    pattern = r'.*외'
                    PostCount = re.sub(pattern, '', PostCount)
                    pattern = r'건.*'
                    PostCount = re.sub(pattern, '', PostCount)
                    pattern = r'&nbsp;'
                    PostCount = re.sub(pattern, '', PostCount)

                    Title = ""
                    Post = self.IncheonPost(page_source, int(PostCount))
                    if Post is not None:
                        print("인천 기사 내용 크롤링 성공")

                self.exeTitle.delete("1.0", tk.END)
                self.exeTitle.insert(tk.END, Title if Title else "제목 가져오기 실패")
                self.exePost.delete("1.0", tk.END)
                self.exePost.insert(tk.END, Post if Post else "내용 가져오기 실패")
        # except Exception as e:
        #     print(f"CrawlingPost에서 오류 발생 : {e}")


    def CopyTitle(self):
        try:
            Title = self.exeTitle.get("1.0", tk.END).strip()
            root.clipboard_clear()
            root.clipboard_append(Title)
        except Exception as e:
            print(f"CopyTItle에서 오류 발생 : {e}")

    def CopyPost(self):
        try:
            Post = self.exePost.get("1.0", tk.END).strip()
            root.clipboard_clear()
            root.clipboard_append(Post)
        except Exception as e:
            print(f"CopyPost에서 오류 발생 : {e}")

    def trafilaPost(self, url : str, event = None):
        """
        url 에 있는 내용을 크롤링하여 html 태그를 지워
        필요한 내용을 좀 더 간결하게 볼 수 있도록 하는 함수입니다.
        """
        try:
            #변수 url에 저장되어있는 링크를 통해 기사를 가져옴(정리되어있지 않음)
            PostLink = trafilatura.fetch_url(url, config=config)

            #PostLink에 저장되어있는 데이터 중 필요한 내용을 추출(본문 기사)
            MainPost = trafilatura.extract(PostLink, config=config)

            return MainPost
        except Exception as e:
            print(f"TrafilaPost에서 오류 발생 : {e}")

    def SeoulTitle(self, url : str):
        """
        서울교육청 보도자료의 날짜, 기자정보 등을 반환합니다.
        """
        try:
            MainPost = trafilatura.fetch_url(url, config=config)

            if MainPost:
                #제목 앞쪽의 필요없는 부분 제거
                MainPost = re.sub(r".*\$\(\"head title\"\)\.replaceWith\(\'\<title\>", '', MainPost, flags=re.DOTALL)
                #제목 뒤쪽의 필요없는 부분 제거
                MainPost = re.sub(r"ㅣ.*", '', MainPost, flags=re.DOTALL)
                return MainPost
            else:
                print("잘못된 url입니다.")
        except Exception as e:
            print(f"SeoulTitle에서 오류 발생 : {e}")

    def FindSeoulReporter(self, url : str):
        """
        서울교육청 보도자료의 기자를 찾아 반환합니다.
        """
        try:
            MainPost = trafilatura.fetch_url(url, config=config)

            if MainPost:
                MainPost = re.sub(r".*\<div class\=\"view_tit\"\>", '', MainPost, flags=re.DOTALL)
                MainPost = re.sub(r"\<\/p\>.*", '', MainPost, flags=re.DOTALL)
                MainPost = re.sub(r".*\<\/strong\>", '', MainPost, flags=re.DOTALL)
                MainPost = re.sub(r".*\<p\>", '', MainPost, flags=re.DOTALL)

                return MainPost
            else:
                print("잘못된 url입니다.")
        except Exception as e:
            print(f"FindSeoulReporter에서 오류 발생 : {e}")

    def SeoulPost(self, url : str):
        """
        서울교육청 보도자료에서 크롤링된 내용 중\n
        기사내용을 가져오는 함수입니다.
        """
        try:
            MainPost = self.trafilaPost(url)

            if MainPost:
                #기자정보 항목 제거
                reporter = self.FindSeoulReporter(url)
                if reporter:
                    MainPost = re.sub(reporter, '', MainPost, flags=re.DOTALL)

                    #re.sub('찾으려는 문자', '대체하려는 문자', 위치)
                    #ex) re.sub('abc','bca',text) -> text 변수 내 abc라는 문자를 bca로 대체
                    MainPost = re.sub(r'\(http\S+\)', '', MainPost)

                    #기사 내 누리집(링크)가 있을 경우 링크를 제거
                    MainPost = re.sub(r'누리집\(\S+\)', '누리집', MainPost)

                    #서울시 기사의 문장 시작에 붙는 ▢, ○ 등을 제거
                    MainPost = re.sub('[□▢○❍◯〇▲△▸▶]', '', MainPost)

                    #붙임 항목 포함한 뒤의 내용을 제거
                    Attached = r'붙임.*|\[붙임.*'
                    MainPost = re.sub(Attached, '', MainPost, flags=re.DOTALL)

                    #저작권 항목 제거
                    copyright = r'\[Copyrights ⓒ 서울교육소식 \(enews\.sen\.go\.kr\) 배포시 저작자 반드시 표기\].*'
                    #re.DOTALL를 통해 줄바꿈이 일어나도 뒤의 내용을 제거하도록 함
                    MainPost = re.sub(copyright, '', MainPost, flags=re.DOTALL)

                    return MainPost
                else:
                    print("reporter : X")
            else:
                print("잘못된 url입니다.")
        except Exception as e:
            print(f"SeoulPost에서 오류 발생 : {e}")

    def GyeonggidoTitle(self, url : str):
        """
        경기도교육청 보도자료에서 크롤링된 내용 중\n
        제목을 가져오는 함수입니다.
        """
        try:
            Title = self.trafilaPost(url)

            if Title:
                #제목 이전 불필요한 텍스트 제거
                Title = re.sub(r".*?제목 \|",'', Title, flags=re.DOTALL)
                #제목 이후 불필요한 텍스트 제거
                Title = re.sub(r"작성자.*", '', Title, flags=re.DOTALL)
                Title = re.sub(r"\| \|", '', Title)
                Title = re.sub(r"\n", '', Title)
                return Title
            else:
                print("잘못된 url입니다.")
        except Exception as e:
            print(f"GyeonggidoTitle에서 오류 발생 : {e}")

    def GyeonggidoPost(self, url : str):
        """
        경기도교육청 보도자료에서 크롤링된 내용 중\n
        기사내용을 가져오는 함수입니다.
        """
        try:
            MainPost = self.trafilaPost(url)

            if MainPost:
                #내용 이전 불필요한 텍스트 제거
                MainPost = re.sub(r".*내용 \|",'', MainPost, flags=re.DOTALL)
                #내용 이후 불필요한 텍스트 제거
                MainPost = re.sub(r"담당자.*",'', MainPost, flags=re.DOTALL)
                MainPost = re.sub(r"\* 문의.*",'', MainPost, flags=re.DOTALL)
                MainPost = re.sub(r"\|",'', MainPost, flags=re.DOTALL)

                #내용 중 url 제거
                MainPost = re.sub(r'\(http\S+\)', '', MainPost)
                MainPost = re.sub(r'누리집\(\S+\)', '누리집', MainPost)

                #내용 중 특수문자 제거
                MainPost = re.sub('[□▢○❍◯〇▲△▸▶]', '', MainPost)
                
                return MainPost
        except Exception as e:
            print(f"GyeonggidoPost에서 오류 발생 : {e}")

    def IncheonPost(self, page_source : str, postcount : int):
        """
        인천교육청 보도자료에서 크롤링된 내용 중\n
        기사내용을 가져오는 함수입니다.
        """
        try:
            Mainpost = ""
            for i in range(postcount + 2):

                j = i + 1

                # 제목 이전 불필요한 텍스트 제거
                prepost = rf".*?{i}\. "
                tmp = re.sub(prepost, "", page_source, flags=re.DOTALL)

                # 제목 이후 불필요한 텍스트 제거
                pospost = rf"{j}\. .*"
                tmp = re.sub(pospost, "", tmp, flags=re.DOTALL)

                #기사 내 URL 제거
                tmp = re.sub(r'\(http\S+\)', '', tmp)
                tmp = re.sub(rf'누리집\(\S+\)', '누리집', tmp)

                #기사 내 전화번호 제거
                tmp = re.sub(r'\(\s*☎\s*(\d{3}-\d{4}|\d{3}-\d{3}-\d{4}|\d{2}-\d{3}-\d{4}|\d{3}-\d{4}-\d{4})\s*\)', '', tmp)
                
                #제목 이후 불필요한 텍스트 제거
                tmp = re.sub('[□▢○❍◯〇▲△▸▶]', '', tmp)
                
                Mainpost += tmp + "\n\n"
            return Mainpost
        except Exception as e:
            print(f"IncheonPost에서 오류 발생 : {e}")

    def contain_char(self, string : str, char : str):
        """
        string 문자열 내에 char가 있는지 확인합니다.\n
        현재 코드에서는 url 내 특정 url이 있을 경우, \n
        그에 해당하는 사이트로 판정합니다.
        """
        return char in string

if __name__ == "__main__":
    root = tk.Tk()
    mainChrome = Chromeapp(root)