import trafilatura
from trafilatura.settings import use_config
from trafilatura import extract_metadata
import re
import pyperclip
import requests
from bs4 import BeautifulSoup
import os
import urllib.request

def trafilaPost(url : str):
    """
    url 에 있는 내용을 크롤링하여 html 태그를 지워\n
    필요한 내용을 좀 더 간결하게 볼 수 있도록 하는 함수입니다.
    """
    #변수 url에 저장되어있는 링크를 통해 기사를 가져옴(정리되어있지 않음)
    PostLink = trafilatura.fetch_url(url)
    #PostLink에 저장되어있는 데이터 중 필요한 내용을 추출(본문 기사)
    MainPost = trafilatura.extract(PostLink)

    return PostLink

def SeoulPost(url : str):
    """
    서울교육청 보도자료에서 크롤링된 내용 중\n
    내용을 가져오는 함수입니다.
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
        MainPost = re.sub('[□▢○❍◯〇*▲▸]', '', MainPost)

        #붙임 항목 포함한 뒤의 내용을 제거
        Attached = r'붙임.*|\[붙임.*'
        MainPost = re.sub(Attached, '', MainPost, flags=re.DOTALL)

        #저작권 항목 제거
        copyright = r'\[Copyrights ⓒ 서울교육소식 \(enews\.sen\.go\.kr\) 배포시 저작자 반드시 표기\].*'
        #re.DOTALL를 통해 줄바꿈이 일어나도 뒤의 내용을 제거하도록 함
        MainPost = re.sub(copyright, '', MainPost, flags=re.DOTALL)

        return MainPost
    else:
        print("잘못된 url입니다.")

def FindReporter(url : str):
    """
    서울교육청 보도자료의 기자를 찾아 반환합니다.
    """
    MainPost = trafilatura.fetch_url(url)

    if MainPost:
        #앞쪽의 필요없는 부분 제거
        MainPost = re.sub(r".*\<div class\=\"view_tit\"\>", '', MainPost, flags=re.DOTALL)
        MainPost = re.sub(r"\<\/p\>.*", '', MainPost, flags=re.DOTALL)
        MainPost = re.sub(r".*\<\/strong\>", '', MainPost, flags=re.DOTALL)
        MainPost = re.sub(r".*\<p\>", '', MainPost, flags=re.DOTALL)
        #뒤쪽의 필요없는 부분 제거

        return MainPost
    else:
        print("잘못된 url입니다.")


if __name__ == "__main__":

    
    url = "https://enews.sen.go.kr/news/view.do?bbsSn=186877&step1=3&step2=1"
    
    print(FindReporter(url))