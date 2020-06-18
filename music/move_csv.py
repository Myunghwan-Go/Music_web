import time
import pyperclip
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import csv

def move_to_genie(id, password, list):
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install())

    link='https://www.genie.co.kr/'
    driver.get(link)

    driver.find_element_by_xpath('//*[@id="gnb"]/div/div/button').click() #로그인 하기
    driver.find_element_by_xpath('//*[@id="gnb"]/div/div/div/div/a').click() #지니 로그인
    driver.switch_to.window(driver.window_handles[1]) # 기존 창[0] 말고 아이디 입력창(새로 뜬 창[1])에 focus

    driver.find_element_by_id('gnb_uxd').send_keys(id) #아이디 //*[@id="gnb_uxd"]
    driver.find_element_by_id('gnb_uxx').send_keys(password) #비번
    driver.find_element_by_xpath('//*[@id="f_login_layer"]/input[2]').click() #클릭
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 1) #창 개수가 변할 때 까지 여유 이것때매 느린가
    driver.switch_to.window(driver.window_handles[0]) #다시 원래창으로 (로그인 후 창닫힘)

    count = 0
    notfound = []
    for line in list:
        if line == ['']:
            break
        #print(line)
        driver.find_element_by_xpath('//*[@id="sc-fd"]').send_keys(line[0]) # 제목 가수 앨범 입력
        driver.find_element_by_xpath('//*[@id="frmGNB"]/fieldset/input[3]').click()  # 검색 클릭
        try:
            driver.find_element_by_xpath('//*[@id="add_my_album_list"]')
            driver.find_element_by_xpath('//*[@id="body-content"]/div[3]/div[2]/div/table/tbody/tr[1]/td[1]/input').click() # 체크 버튼
            driver.find_element_by_xpath('//*[@id="add_my_album_list"]').click()                        # 담기 버튼 클릭
            if count == 0:
                savename = str(datetime.today()).replace(' ', '_')
                driver.find_element_by_xpath('/html/body/div[4]/div[1]/input').send_keys(savename[:19]+'_New')
                driver.find_element_by_xpath('/html/body/div[4]/div[1]/button').click()  # 체크 버튼
                value = savename[:19]+'_New'
                count += 1
                time.sleep(0.5)
            driver.find_element_by_xpath('//*[@title="%s"]' % (value)).click()                 # move 플레이리스트
            time.sleep(0.5)
            Alert(driver).accept()                                                                      # 경고창 처리
            driver.find_element_by_xpath('//*[@id="sc-fd"]').clear()                                    # 검색창 초기화
            time.sleep(0.5)
        except NoSuchElementException:
            #print(line, "can't found")
            notfound.append(''.join(line))#.replace(",  ", " - ", 1))
            driver.find_element_by_xpath('//*[@id="sc-fd"]').clear()                                    # 검색창 초기화
            time.sleep(0.5)
        except NoAlertPresentException:
            time.sleep(0.5)
            Alert(driver).accept()
            driver.find_element_by_xpath('//*[@id="sc-fd"]').clear()                                    # 검색창 초기화
            time.sleep(0.5)
        if notfound is None:
            notfound.append('누락된 곡이 없습니다.')
    driver.quit()
    return notfound


def move_to_melon(id, password, list):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.melon.com/')
    driver.find_element_by_xpath('//*[@id="gnbLoginDiv"]/div/button/span').click()
    driver.find_element_by_xpath('//*[@id="conts_section"]/div/div/div[1]/button').click() # 카카오
    #driver.find_element_by_xpath('//*[@id="conts_section"]/div/div/div[2]/button').click() #멜론
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
    driver.switch_to.window(driver.window_handles[1])

    driver.find_element_by_id('id_email_2').send_keys(id)  # 카카오 # 여기에 아이디 입력
    driver.find_element_by_id('id_password_3').send_keys(password)  # 여기에 비밀번호
    #driver.find_element_by_id('id').send_keys(id) # 멜론 # 여기에 아이디 입력
    #driver.find_element_by_id('pwd').send_keys(password) # 여기에 비밀번호
    driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div/button').click()  # 카카오 로그인
    #driver.find_element_by_xpath('//*[@id="conts_section"]/div/div/div[2]/button').click() # 멜론
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 1)
    driver.switch_to.window(driver.window_handles[0])

    # 주석 처리 한 부분은 카카오 로그인 시 필요한 부분 (14,16,17,19,20,23,25,26 라인) / 멜론 로그인 하려면 (15,21,22,24 라인 사용)

    driver.find_element_by_xpath('//*[@id="top_search"]').send_keys('a')
    #driver.find_element_by_id('top_search').send_keys('a')
    driver.find_element_by_xpath('//*[@id="gnb"]/fieldset/button[2]/span').click() # 메인 검색창과 곡 검색 후 버튼의 이름이 달라 통일 작업
    driver.find_element_by_xpath('//*[@id="top_search"]').clear()

    notfound = []
    count = 0
    for line in list:
        if line == ['']:
            break
        if count == 0:
            #print(line)
            driver.find_element_by_xpath('//*[@id="top_search"]').send_keys(line[0])  # 제목 가수 앨범 입력
            driver.find_element_by_xpath('//*[@id="header_wrap"]/div[3]/fieldset/button[2]').click()  # 검색

            try:
                driver.find_element_by_xpath('//*[@id="divCollection"]/ul/li[3]').click()  # 곡으로 이동
                driver.find_element_by_xpath(
                    '//*[@id="frm_defaultList"]/div/table/tbody/tr[1]/td[3]/div/div/button[2]').click()
                WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
                driver.switch_to.window(driver.window_handles[1])  # 창 전환
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/div/div/div[2]/button').click()  # 플레이 리스트 만들기 클릭
                time.sleep(0.5)
                WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
                driver.switch_to.window(driver.window_handles[1])  # 창 전환
                savename = str(datetime.today())
                driver.find_element_by_xpath('//*[@id="plylstTitle"]').send_keys(savename[:19]+'_New')  #입력
                count += 1
                driver.find_element_by_xpath('/html/body/div/div/div[2]/button[1]').click()
                WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
                driver.switch_to.window(driver.window_handles[1])  # 창 전환
                driver.find_element_by_xpath('/html/body/div/div/div[2]/button/span/span').click()
                WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 1)
                driver.switch_to.window(driver.window_handles[0])
                driver.find_element_by_xpath('//*[@id="top_search"]').clear()  # 검색 창 초기화

            except NoSuchElementException:
                #print(line, "can't found")
                notfound.append(''.join(line).replace(",", " -", 1))
                driver.find_element_by_xpath('//*[@id="top_search"]').clear()  # 검색 창 초기화
                time.sleep(0.5)

        else:
            #print(line)
            driver.find_element_by_xpath('//*[@id="top_search"]').send_keys(line[0])   # 제목 가수 앨범 입력
            driver.find_element_by_xpath('//*[@id="header_wrap"]/div[3]/fieldset/button[2]').click() # 검색


            try:
                driver.find_element_by_xpath('//*[@id="divCollection"]/ul/li[3]').click() # 곡으로 이동
                driver.find_element_by_xpath('//*[@id="frm_defaultList"]/div/table/tbody/tr[1]/td[3]/div/div/button[2]').click()
                WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
                driver.switch_to.window(driver.window_handles[1]) # 창 전환
                driver.find_element_by_xpath('//*[@id="plylstList"]/div/table/tbody/tr/td[1]/div/div/span').click() # 제목 클릭해 선택 보이기
                driver.find_element_by_xpath('//*[@id="plylstList"]/div/table/tbody/tr/td[1]/div/span/button').click() # 선택 클릭
                time.sleep(0.5)

                try:
                    Alert(driver).accept()  # 만약 이미 담은 곡이면 경고창 처리
                    # 이미 담은 곡이면 Alert뜨고 창 변화 없으므로 닫아주기
                    driver.close()
                #                    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 1)
                #                    driver.switch_to.window(driver.window_handles[0])
                #                    driver.find_element_by_xpath('//*[@id="top_search"]').clear()  # 검색 창 초기화
                except:
                    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
                    driver.switch_to.window(driver.window_handles[1])
                    driver.find_element_by_xpath('/html/body/div/div/div[2]/button/span/span').click()  # 창 전환해서 확인 누르기

                WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 1)
                driver.switch_to.window(driver.window_handles[0])  # 맨 처음 창으로 전환
                driver.find_element_by_xpath('//*[@id="top_search"]').clear()  # 검색 창 초기화

            except NoSuchElementException:
                 #print(line, "can't found")
                 notfound.append(''.join(line))#.replace(",  ", " - ", 1))
                 driver.find_element_by_xpath('//*[@id="top_search"]').clear()  # 검색 창 초기화
                 time.sleep(0.5)
        if notfound is None:
            notfound.append('누락된 곡이 없습니다.')
    driver.quit()
    return notfound


def move_to_flo(id, password, list):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.music-flo.com/')
    #driver.find_element_by_xpath('//*[@id="header"]/div/div/ul/li[2]/a').click()  # 로그인 href="/member/signin"
    driver.find_element_by_xpath('//*[@href="/member/signin"]').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[2]/a[1]').send_keys('\n')  # T아이디로 로그인
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])  # 로그인 창으로 전환
    driver.find_element_by_xpath('//*[@id="userId"]').send_keys(id) # 여기에 아이디 입력
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password) # 여기에 비밀번호
    driver.find_element_by_xpath('//*[@id="authLogin"]').click()
    driver.switch_to.window(driver.window_handles[0])  # 페이지로 전환
    time.sleep(1)
    driver.get('https://www.music-flo.com/search/all?keyword')
    time.sleep(1)

    count = 0
    notfound = []
    for line in list:
        if line == ['']:
            break
        try:
            #print(line)
            driver.find_element_by_xpath('//*[@id="searchKeywordInput"]').send_keys(line[0], Keys.ENTER)
            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/div/div[2]/div[3]/button[2]').click() # 리스트 담기
            if count == 0:
                time.sleep(0.5)
                savename = str(datetime.today())
                driver.find_element_by_xpath('//*[@id="app"]/div[4]/div/div/ul/li[1]/button/div[2]/div/p').click()
                driver.find_element_by_xpath('/html/body/div/div[4]/div/div/ul/li[1]/div/div/label/input').send_keys(savename[:19] + '_New')
                count += 1
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/div/div[4]/div/div/ul/li[1]/div/p/button[2]').click()

            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="app"]/div[4]/div/div/ul/li[2]/button').click()
            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="header"]/div/fieldset/button').click() # 검색 창 내용 삭제
            time.sleep(0.5)

        except NoSuchElementException:
            #print(line, "can't found")
            notfound.append(''.join(line))#.replace(",  ", " - ", 1))
            driver.find_element_by_xpath('//*[@id="header"]/div/fieldset/button').click()
            time.sleep(0.5)

        if notfound is None:
            notfound.append('누락된 곡이 없습니다.')
    driver.quit()
    return notfound


def move_to_bugs(id, password, list):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://music.bugs.co.kr/')
    driver.find_element_by_xpath('//*[@id="loginHeader"]/a').click()
    driver.find_element_by_xpath('//*[@id="payco-auth-popup"]').click()  # PAYCO로 로그인
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
    driver.switch_to.window(driver.window_handles[1])

    driver.find_element_by_xpath('//*[@id="id"]').send_keys(id) # 여기에 아이디 입력
    driver.find_element_by_xpath('//*[@id="pw"]').send_keys(password) # 여기에 비밀번호
    driver.find_element_by_xpath('//*[@id="loginBtn"]').click()
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 1)
    driver.switch_to.window(driver.window_handles[0])
    # 로그인
    count = 0
    notfound = []
    for line in list:
        if line == ['']:
            break
        try:
            #print(line)
            driver.find_element_by_xpath('//*[@id="headerSearchInput"]').send_keys(line[0])
            driver.find_element_by_xpath('//*[@id="hederSearchFormButton"]').click()
            driver.find_element_by_xpath('//*[@id="DEFAULT0"]/table/tbody/tr[1]/td[8]/a').click()
            if count == 0:
                savename = str(datetime.today())
                time.sleep(0.5)

                driver.find_element_by_xpath('/html/body/aside[1]/div[2]/div/div/ul/li[1]/a').click()
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/aside[3]/section/fieldset/div[1]/div/input').clear()
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/aside[3]/section/fieldset/div[1]/div/input').send_keys(savename[:19] + '_New')
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/aside[3]/section/fieldset/div[2]/button[1]').click()
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/aside[4]/section/p/button').click()
                count += 1
                driver.find_element_by_xpath('//*[@id="headerSearchInput"]').clear()
                time.sleep(0.5)
            else:
                time.sleep(0.5)
                driver.find_element_by_xpath('//*[@id="track2playlistScrollArea"]/div/div/ul/li[2]/a').click() # 곡 담기
                time.sleep(0.5)
                driver.find_element_by_xpath('//*[@id="bugsAlert"]/section/p/button').click() # 확인
                time.sleep(0.5)
                driver.find_element_by_xpath('//*[@id="headerSearchInput"]').clear()
                time.sleep(0.5)

        except NoSuchElementException:
            #print(line, "can't found")
            notfound.append(''.join(line))#.replace(",  ", " - ", 1))
            driver.find_element_by_xpath('//*[@id="headerSearchInput"]').clear()
            time.sleep(0.5)

        if notfound is None:
            notfound.append('누락된 곡이 없습니다.')
    driver.quit()
    return notfound


def move_to_vibe(id, password, list):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://vibe.naver.com')
    driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/a').click()  # 팝업창 닫기
    driver.find_element_by_xpath('//*[@id="app"]/div/header/div[2]/div[1]/a').click()
    #id = '' # 여기에 아이디 입력
    #pw = '' # 여기에 비밀번호

    copy_input('//*[@id="id"]', id, driver)
    copy_input('//*[@id="pw"]', password, driver)
    #time.sleep(5)
    driver.find_element_by_xpath('//*[@id="log.login"]').click()
    driver.find_element_by_xpath('//*[@id="new.dontsave"]').click()
    # 네이버는 로그인 속도가 너무 빠르면 캡차 요구, 파이썬으로 클립보드 사용하는 방식 이용
    time.sleep(1.5)
    count = 0
    notfound = []
    for line in list:
        if line == ['']:
            break
        try:
            driver.find_element_by_xpath('//*[@id="app"]/div/header/a[1]').click()
            driver.find_element_by_xpath('//*[@id="search_keyword"]').clear()
            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="search_keyword"]').send_keys(line[0], Keys.ENTER) # 검색
            time.sleep(0.5)
            if count == 0:
                savename = str(datetime.today())
                print(savename)
                driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/ div/div[3]/div/div/a').click()
                driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/ div/div[3]/div/div/div/a[2]').click()
                time.sleep(0.5)
                driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div/a[1]').click()
                driver.find_element_by_xpath('//*[@id="new_playlist"]').send_keys(savename[:19] + '_New')
                time.sleep(0.5)
                count += 1
                driver.find_element_by_xpath('//*[@id="app"]/div[3]/div/div/div/a[2]').click()
                time.sleep(0.5)
                driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div/a[3]').click()
                time.sleep(0.5)
                driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div/a').click()
                driver.find_element_by_xpath('//*[@id="app"]/div/header/a[1]').click()
                time.sleep(0.5)
                #driver.find_element_by_xpath('//*[@id="search_keyword"]').clear()
                #time.sleep(0.5)
            else:
                driver.find_element_by_xpath('//*[@id="content"]/div[2]/h3/a').click() # 노래 이동
                time.sleep(0.5)
                driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div/table/tbody/tr[1]/td[8]/div/div/a').click()
                time.sleep(0.5)
                driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div[1]/div/table/tbody/tr[1]/td[8]/div/div/div/a[2]').click()
                time.sleep(0.5)
                driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/a[3]/div[2]/div/em').click() # 추가
                time.sleep(0.5)
                driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/div/a').click() # 확인
                time.sleep(0.5)
                #driver.find_element_by_xpath('//*[@id="app"]/div/header/a[1]').click()
                #time.sleep(0.5)
                #driver.find_element_by_xpath('//*[@id="search_keyword"]').clear()
                #time.sleep(0.5)



        except NoSuchElementException:
            #print(line, "can't found")
            notfound.append(''.join(line))
            driver.find_element_by_xpath('//*[@id="app"]/div/header/a[1]').click()
            time.sleep(0.5)
            #driver.find_element_by_xpath('//*[@id="search_keyword"]').clear()
            #time.sleep(0.5)
        except ElementNotInteractableException:
            #print('ElementNotInteractableException', line)
            time.sleep(0.5)

        if notfound is None:
            notfound.append('누락된 곡이 없습니다.')
    driver.quit()
    return notfound


def copy_input(xpath, input, driver):
    pyperclip.copy(input)
    driver.find_element_by_xpath(xpath).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(0.5)