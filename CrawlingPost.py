import trafilatura
from trafilatura.settings import use_config
import re
import pyperclip
import requests
from bs4 import BeautifulSoup
import os
import urllib.request

def trafilaPost(url):
    #변수 url에 저장되어있는 링크를 통해 기사를 가져옴(정리되어있지 않음)
    PostLink = trafilatura.fetch_url(url)
    #PostLink에 저장되어있는 데이터 중 필요한 내용을 추출(본문 기사)
    MainPost = trafilatura.extract(PostLink)

    return MainPost

def SeoulPost(url):
    """
    서울교육청 보도자료의 기사 내용을 가져옵니다.

    매개변수 : 
    url(str) : 서울교육청 기사 링크
    """
    MainPost = trafilaPost(url)

    if MainPost:
        #http라는 내용이 있을 경우 ()를 포함하여 제거

        #re.sub('찾으려는 문자', '대체하려는 문자', 위치)
        #ex) re.sub('abc','bca',text) -> text 변수 내 abc라는 문자를 bca로 대체
        MainPost = re.sub(r'\(http\S+\)', '', MainPost)

        #기사 내 누리집(링크)가 있을 경우 링크를 제거
        MainPost = re.sub(r'누리집\(\S+\)', '누리집', MainPost)

        #서울시 기사의 문장 시작에 붙는 ▢, ○ 등을 제거
        MainPost = re.sub('[□▢○❍◯▲▸]', '', MainPost)

        #붙임 항목 포함한 뒤의 내용을 제거
        Attached = r'붙임.*|\[붙임.*'
        MainPost = re.sub(Attached, '', MainPost, flags=re.DOTALL)

        #저작권 항목 제거
        copyright = r'\[Copyrights ⓒ 서울교육소식 \(enews\.sen\.go\.kr\) 배포시 저작자 반드시 표기\].*'
        #re.DOTALL를 통해 줄바꿈이 일어나도 뒤의 내용을 제거하도록 함
        MainPost = re.sub(copyright, '', MainPost, flags=re.DOTALL)
        

        pyperclip.copy(MainPost)
        print("클립보드에 복사되었습니다.")

        return MainPost
    else:
        print("잘못된 url입니다.")

def gyeonggidoTitle(url):
    """
    서울교육청 보도자료의 기사 내용을 가져옵니다.

    매개변수 : 
    url(str) : 서울교육청 기사 링크
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
        print("잘못된 url입니다.")

def gyeonggidoPost(url):
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

def contain_char(string, char):
    """
    string 문자열 내에 char가 있는지 확인합니다.
    있을 경우 True, 없을 경우 False로 반환합니다.
    """
    return char in string

def savetxt(Title, MainPost):
    file_path = Title + ".txt"

    # 파일을 쓰기 모드로 열고 문자열을 파일에 작성합니다.
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(MainPost)

    print(f"기사내용이 {file_path}파일에 저장되었습니다.")

def saveimg(url):
    for i in range(10):
        urllib.request.urlretrieve(url, str(i + 1) + ".jpg")

if __name__ == "__main__":

    #기사 링크설정
    url = input("링크를 입력하십시오 : ")

    if contain_char(url, "enews.sen.go.kr"):
        #서울시 기사일 경우
        Post = SeoulPost(url)
    if contain_char(url, "www.goe.go.kr"):
        #경기도 기사일 경우
        Title = gyeonggidoTitle(url)
        Post = gyeonggidoPost(url)
        savetxt(Title, Post)