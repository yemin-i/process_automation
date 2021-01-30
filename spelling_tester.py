#!/usr/bin/env python
# coding: utf-8

# In[12]:


# 라이브러리
from selenium import webdriver # 웹 브라우저를 제어할 웹드라이버
from selenium.webdriver.common.keys import Keys # 키보드 입력을 위해 가져오는 기능
import time  # 시간 관련 라이브러리
from bs4 import BeautifulSoup # html과 xml 파싱하는 기능


# In[31]:


# 파일 불러오기
def load_file():
    file = open('C:/Users/user/Desktop/test_text.txt', 'r', encoding = 'utf-8')
    text = file.read()
    file.close()
    return text

# 500자 길이로 텍스트 나누기
def text_split(text):
    ready_list = []
    while len(text) > 500:  # text 길이가 500자 초과이면,
        temp_str = text[:500]  # temp_str 이라는 임시 변수에 500자까지만 저장
        last_space = temp_str.rfind(' ') # 가장 가까운 공백 찾기. find는 왼쪽부터 공백을 찾기 때문에 가장 먼 공백이 출력됨.
        temp_str = text[0:last_space]  # 가장 가까운 공백의 인덱스를 슬라이싱함.
        ready_list.append(temp_str)    # 슬라이싱 결과를 ready_list에 저장
        text = text[last_space:]      # 이전 글은 삭제하기 위해 last_space 를 첫 인덱스로 둠. 
    # 500자에 못 들어간 나머지 텍스트를 ready_list에 저장
    ready_list.append(text)
    
    return ready_list

# 셀레니움으로 맞춤법 검사하기
def run_test(ready_list):
    driver = webdriver.Chrome('C:/js/chromedriver.exe')
    driver.get('http://naver.com')

    elem = driver.find_element_by_name('query')  # 네이버 검색창에 해당하는 name 찾기

    elem.send_keys('맞춤법 검사기')   # 검색창에 '맞춤법 검사기' 단어 입력
    # elem.send_keys(Keys.RETURN)
    elem.submit()   # 검색 실행

    time.sleep(2)   
    textarea = driver.find_element_by_class_name('txt_gray')  # 맞춤법 검사기 창에 해당하는 class name 찾기

    new_str = ''
    # 500자 단위로 분리된 텍스트로 검사 진행
    for i in ready_list:
        textarea.send_keys(Keys.CONTROL, 'a')  # ctrl + a 기능으로 검사창 초기화
        textarea.send_keys(i)

        elem = driver.find_element_by_class_name('btn_check')
        elem.click()

        time.sleep(1)
        # 맞춤법 검사 후 화면의 소스코드 가져오기
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # soup.select('p._result_text.stand_txt')[0] 는 리스트 형태로 출력되므로 text 기능을 활용하려면 
        # str 타입으로 가져와야 해서 인덱싱을 함
        st = soup.select('p._result_text.stand_txt')[0].text
        new_str += st.replace('.', '.\n')
    return new_str

# 맞춤법 검사한 text를 txt파일로 저장하기
def create_txt_file(new_str):
    file = open('C:/Users/user/Desktop/result.txt', 'w', encoding = 'utf-8')
    file.write(new_str)
    file.close()
    return file

