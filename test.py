import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

import trafilatura
from trafilatura.settings import use_config

import pygetwindow
from pywinauto import Desktop
from bs4 import BeautifulSoup
import requests
import pyperclip
import time
import re

def trafilaPost(url : str):
    """
    url 에 있는 내용을 크롤링하여 html 태그를 지워\n
    필요한 내용을 좀 더 간결하게 볼 수 있도록 하는 함수입니다.
    """
    #변수 url에 저장되어있는 링크를 통해 기사를 가져옴(정리되어있지 않음)
    PostLink = trafilatura.fetch_url(url)
    #PostLink에 저장되어있는 데이터 중 필요한 내용을 추출(본문 기사)
    MainPost = trafilatura.extract(PostLink)

    return MainPost

class Chromeapp:
    def __init__(self, root):
        """
        GUI 구현
        """
        self.root = root
        self.driver = None

        # OpenChrome()
        self.root.title("test")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.root.grid_rowconfigure(0, minsize=100)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=2)

        self.root.grid_columnconfigure(0, minsize=100)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        Incheon = tk.Button(root, text="인천")
        Incheon.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        Seoul = tk.Button(root, text="서울")
        Seoul.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.Geonggido = tk.Button(root, text="경기", command=self.OpenGeonggido)
        self.Geonggido.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        CopyPost = tk.Button(root, text="크롬 기사 복사", command=self.CrawlingGyeonggido)
        CopyPost.grid(row=0, column=3, sticky="nsew", padx=10, pady=10)

        self.exeTitle = tk.Text(root, height=2, width=50)
        self.exeTitle.grid(row=1,column = 0, columnspan = 3, sticky="nsew", padx=10, pady=10)

        TitleCopy = tk.Button(root, text="제목 복사")
        TitleCopy.grid(row=1, column=3, sticky="nsew", padx=10, pady=10)

        self.exePost = tk.Text(root, height=16, width=40)
        self.exePost.grid(row=2,column = 0, columnspan = 3, sticky="nsew", padx=10, pady=10)


        PostScroll = tk.Scrollbar(root, orient="vertical", command=self.exePost.yview)
        PostScroll.grid(row=2,column=2,columnspan=3, sticky="ns")

        self.exePost.config(yscrollcommand=PostScroll.set)

        PostCopy = tk.Button(root, text="내용 복사")
        PostCopy.grid(row=2, column=3, sticky="nsew", padx=10, pady=10)

        self.root.mainloop()


    def OpenGeonggido(self):
        #webdriver_manager를 이용해 크롬 드라이버를 자동 설치/업데이트 후 실행
        option = Options()
        option.add_experimental_option("detach", True)
        # service = Service(ChromeDriverManager().install())
        service = Service()
        self.driver = webdriver.Chrome(service=service, options=option)
        url = f"https://www.goe.go.kr/home/bbs/bbsList.do?menuId=100000000000059&bbsMasterId=BBSMSTR_000000000163&menuInit=2,2,0,0,0&searchCategory=%EB%8F%84%EA%B5%90%EC%9C%A1%EC%B2%AD"
        self.driver.get(url)


    def CrawlingGyeonggido(self):
        if self.driver:
            current_url = self.driver.current_url
            print(current_url)
            Title = gyeonggidoTitle(current_url)
            Post = gyeonggidoPost(current_url)

            self.exeTitle.delete("1.0", tk.END)
            self.exeTitle.insert(tk.END, Title)
            self.exePost.delete("1.0", tk.END)
            self.exePost.insert(tk.END, Post)


def gyeonggidoTitle(url : str):
    """
    경기도교육청 보도자료에서 크롤링된 내용 중\n
    제목을 가져오는 함수입니다.
    """
    Title = trafilaPost(url)

    if Title:
        #제목 이전 불필요한 텍스트 제거
        Title = re.sub(r".*?제목 \|",'', Title, flags=re.DOTALL)
        #제목 이후 불필요한 텍스트 제거
        Title = re.sub(r"작성자.*", '', Title, flags=re.DOTALL)
        Title = re.sub(r"\| \|", '', Title)
        Title = re.sub(r"\n", '', Title)
        
        return Title
    else:
        return "잘못된 URL 입니다."


def gyeonggidoPost(url : str):
    """
    경기도교육청 보도자료에서 크롤링된 내용 중\n
    기사내용을 가져오는 함수입니다.
    """
    MainPost = trafilaPost(url)

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

        return MainPost

def contain_char(string : str, char : str):
    """
    string 문자열 내에 char가 있는지 확인합니다.\n
    현재 코드에서는 url 내 특정 url이 있을 경우, \n
    그에 해당하는 사이트로 판정합니다.
    """
    return char in string






if __name__ == "__main__":
    root = tk.Tk()
    mainChrome = Chromeapp(root)
    