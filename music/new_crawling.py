import os
from bs4 import BeautifulSoup
from prompt_toolkit.clipboard import pyperclip
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import csv, random, time
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip
import clipboard

from selenium.webdriver.common.keys import Keys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings")
import django
django.setup()
from music.models import Mdg


def get_music(site, id, password):
    user = random.randint(0, 1000000)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    #driver: WebDriver = webdriver.Chrome('./chromedriver',chrome_options=options)
    driver = webdriver.Chrome(ChromeDriverManager().install() )
    if site == 'genie':
        get_from_genie(id, password, user, driver)
    if site == 'flo':
        get_from_flo(id, password, user, driver)
    if site == 'melon':
        get_from_melon(id, password, user, driver)
    if site == 'bugs':
        get_from_bugs(id, password, user, driver)
    if site == 'vibe':
        get_from_vibe(id, password, user, driver)
    driver.quit()
    return user

def get_from_genie(id, password, user, driver):
    driver.get('https://www.genie.co.kr')
    driver.find_element_by_xpath('//*[@id="gnb"]/div/div/button').click()
    driver.find_element_by_xpath('//*[@id="gnb"]/div/div/div/div/a').click()
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_id('gnb_uxd').send_keys(id)
    driver.find_element_by_id('gnb_uxx').send_keys(password)
    driver.find_element_by_xpath('//*[@id="f_login_layer"]/input[2]').click()
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 1)
    driver.switch_to.window(driver.window_handles[0])
    # 로그인

    driver.get('https://www.genie.co.kr/myMusic/myMusicPlayList') # 마이뮤직으로 이동
    driver.find_element_by_xpath('//*[@id="body-content"]/div[3]/ul/li[1]/div[1]/a[1]').click()
    # 맨 첫번째 위치한 플레이리스트 크롤링

    html = driver.page_source
    parse = BeautifulSoup(html, 'html.parser')
    # print(parse)

    parse_titles = parse.find_all("a", {"class": "title ellipsis"})
    parse_singers = parse.find_all("a", {"class": "artist ellipsis"})
    parse_albums = parse.find_all("a", {"class": "albumtitle ellipsis"})

    title = []
    singer = []
    album = []

    #print(parse_titles)

    for t in parse_titles:
        if 'TITLE' in t.text:
            #print(t, 999)
            title.append(t.text.strip().split('\t\t\t\t\t\t\t\t')[3])  # 앨범 타이틀 곡 일시 나오는 TITLE 출력 제거
        elif '19금' in t.text:
            title.append(t.text.replace('19금', '').strip())
        else:
            title.append(t.text.strip())  # 양쪽 공백 제거

    for s in parse_singers:
        singer.append(s.text.strip())

    for a in parse_albums:
        album.append(a.text.strip())

    # print("T",title)
    # print("S",singer)
    # print("A",album)
    path = "C:/It's_time"
    if not os.path.isdir(path):
        os.mkdir(path)
    csvfile = open("C:/It's_time/Genie_Playlist.csv", "w", encoding='UTF-8')
    csvwriter = csv.writer(csvfile, delimiter='\\')

    for i in range(len(title)):
        #print('%3d번: %s [%s] - %s' % (i + 1, title[i], album[i], singer[i]))
        Mdg.objects.create(song=title[i], album=album[i], artist=singer[i][:45], user_num=user, site_code='G')
        csvwriter.writerow([title[i], singer[i]])

    csvfile.close()
    driver.close()


def get_from_flo(id, password, user, driver):
    driver.get('https://www.music-flo.com/')
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="app"]/div[4]/div/button').click() # 안내 창 닫기
    driver.find_element_by_xpath('//*[@id="header"]/div/div/ul/li[2]/a').click() # 로그인
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[2]/a[1]').send_keys('\n') # T아이디로 로그인
    time.sleep(0.8)
    driver.switch_to.window(driver.window_handles[1]) # 로그인 창으로 전환
    driver.find_element_by_xpath('//*[@id="userId"]').send_keys(id) # 여기에 아이디 입력
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password) # 여기에 비밀번호
    driver.find_element_by_xpath('//*[@id="authLogin"]').click()
    driver.switch_to.window(driver.window_handles[0]) # 페이지로 전환
    time.sleep(1)
    driver.get('https://www.music-flo.com/storage/mylist')
    time.sleep(0.2)
    driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/ul/li[1]/div/div[2]/div[1]/p/a').click()
    time.sleep(0.2)

    html = driver.page_source
    parse = BeautifulSoup(html, 'html.parser')

    parse_titles = parse.find_all("p", {"class": "tit"})
    parse_singers = parse.find_all("span", {"class": "artist_link", "index":"0"})
    parse_albums = parse.find_all("p", {"class": "album"})

    # print(parse_titles)
    # print(parse_albums)
    title = []
    singer = []
    album = []

    for t in parse_titles:
        if '성인' in t.text:
            title.append(t.text.replace('성인', '').strip())
        else:
            title.append(t.text.strip())  # 양쪽 공백 제거

    for s in parse_singers:
        singer.append(s.text.strip())
        # try:
        #     singer.append(s.find("a").text)
        # except AttributeError:
        #     singer.append('Various Artists')

    for a in parse_albums:
        album.append(a.text.strip())

    # print("T",title)
    # print("S",singer)
    # print("A",album)
    path = "C:/It's_time"
    if not os.path.isdir(path):
        os.mkdir(path)
    csvfile = open("C:/It's_time/FLO_Playlist.csv", "w", encoding='UTF-8')
    csvwriter = csv.writer(csvfile, delimiter='\\')

    for i in range(len(title)):
        # print('%3d번: %s [%s] - %s' % (i + 1, title[i], album[i], singer[i]))
        Mdg.objects.create(song=title[i], album=album[i], artist=singer[i], user_num=user, site_code='F')
        csvwriter.writerow([title[i], singer[i]])

    csvfile.close()


def get_from_melon(id, password, user, driver):
    driver.get('https://www.melon.com/')
    driver.find_element_by_xpath('//*[@id="gnbLoginDiv"]/div/button/span').click()
    driver.find_element_by_xpath('//*[@id="conts_section"]/div/div/div[1]/button').click()
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
    driver.switch_to.window(driver.window_handles[1])

    driver.find_element_by_id('id_email_2').send_keys(id)  # 카카오 # 여기에 아이디 입력
    driver.find_element_by_id('id_password_3').send_keys(password)  # 여기에 비밀번호
    # driver.find_element_by_id('id').send_keys('') # 멜론 # 여기에 아이디 입력
    # driver.find_element_by_id('pwd').send_keys('') # 여기에 비밀번호
    driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div/button').click()  # 카카오 로그인
    # driver.find_element_by_xpath('//*[@id="conts_section"]/div/div/div[2]/button').click() # 멜론
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 1)
    driver.switch_to.window(driver.window_handles[0])
    #로그인

    # 주석 처리 한 부분은 카카오 로그인 시 필요한 부분 (14,16,17,19,20,23,25,26 라인) / 멜론 로그인 하려면 (15,21,22,24 라인 사용)

    driver.find_element_by_xpath('//*[@id="gnb_menu"]/ul[2]/li[1]/a/span[2]').click()  # 멜론 홈 -> 마미유직
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="conts"]/div[1]/ul/li[3]/a/span').click()  # 마이뮤직 -> 플레이리스트
    driver.find_element_by_xpath('//*[@id="pageList"]/table/tbody/tr[1]/td[2]/div/div/dl/dt/a').click()  # 맨 처음 플레이리스트
    time.sleep(0.5)

    html = driver.page_source
    parse = BeautifulSoup(html, 'html.parser')

    parse_titles = parse.find_all("a", {"class": "fc_gray"})  # 제목
    parse_singers = parse.find_all("div", {"id": "artistName"})  # 가수
    parse_albums = parse.find_all("div", {"class": "ellipsis"})  # 앨범
    parse_btn = parse.find_all("a", {"class": "btn btn_icon_detail"}) # 장르

    title = []  # 제목
    singer = []  # 가수
    album = []  # 앨범
    genre = []
    acnt = 0  # 앨범 이름 저장용

    for t in parse_titles:
        title.append(t.text)

    for s in parse_singers:
        if s.find('a', {"class": "fc_mgray"}) not in s:
            singer.append('Various Artists')
        else:
            singer.append(s.find('a', {"class": "fc_mgray"}).text)

    for a in parse_albums:
        acnt += 1
        if acnt % 3 == 0:  # div.ellipsis<-이것이 노래, 가수, 앨범 div 모두 동일함. 3번째가 앨범이니 %3==0으로 앨범만 나오도록 처리
            album.append(a.find('a',{"class":"fc_mgray"}).text)
    i = 0
    for g in parse_btn:
        i += 1
        driver.find_element_by_xpath("//*[@id='frm']/div/table/tbody/tr[" + str(i) + "]/td[3]/div/div/a[1]").click()
        genres = driver.find_element_by_xpath("//*[@id='downloadfrm']/div/div/div[2]/div[2]/dl/dd[3]").text
        genre.append(genres)
        driver.back()
    # print("T",title)
    # print("S",singer)
    # print("A",album)

    path = "C:/It's_time"
    if not os.path.isdir(path):
        os.mkdir(path)
    csvfile = open("C:/It's_time/Melon_Playlist.csv", "w", encoding='UTF-8')
    csvwriter = csv.writer(csvfile, delimiter='\\')

    for i in range(len(title)):
        #print('%3d번: %s [%s] - %s %s' % (i+1, title[i], album[i], singer[i], genre[i]))# 곡, 가수, 앨범 순으로 저장
        Mdg.objects.create(song=title[i], album=album[i], artist=singer[i], genre=genre[i], user_num=user, site_code='M')
        csvwriter.writerow([title[i], singer[i]])

    csvfile.close()


def get_from_bugs(id, password, user, driver):
    driver.get('https://music.bugs.co.kr/')
    driver.find_element_by_xpath('//*[@id="loginHeader"]/a').click()
    driver.find_element_by_xpath('//*[@id="payco-auth-popup"]').click() # PAYCO로 로그인
    #driver.find_element_by_xpath('//*[@id="to_bugs_login"]').click() # 벅스 아이디로 로그인 둘 중 맞는걸로 골라서 쓸 것
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
    driver.switch_to.window(driver.window_handles[1])

    driver.find_element_by_xpath('//*[@id="id"]').send_keys(id) # 여기에 아이디 입력
    driver.find_element_by_xpath('//*[@id="pw"]').send_keys(password) # 여기에 비밀번호
    driver.find_element_by_xpath('//*[@id="loginBtn"]').click()
    WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 1)
    driver.switch_to.window(driver.window_handles[0])
    # 로그인
    driver.get('https://music.bugs.co.kr/user/library/myalbum/list')
    driver.find_element_by_xpath('//*[@id="myAlbumListAjax"]/li/figure/figcaption/a[1]').click()
    time.sleep(0.5)

    html = driver.page_source
    parse = BeautifulSoup(html, 'html.parser')

    parse_titles = parse.find_all("p", {"class": "title"})
    parse_singers = parse.find_all("p", {"class": "artist"})
    parse_albums = parse.find_all("a", {"class": "album"})

    title = []
    singer = []
    album = []

    for t in parse_titles:
        if "[권리없는 곡]" in t.text:
            title.append(t.text.replace("[권리없는 곡]", "").strip())
        elif "[19금]" in t.text:
            title.append(t.text.replace("[19금]", "").strip())
        else:
            title.append(t.text.strip())  # 양쪽 공백 제거

    for s in parse_singers:
        if '\n\n\n' in s.text:
            singer.append(s.text.strip().split('\n\n\n')[0])  # 아티스트가 둘 이상이면 \n문제 발생 한명만 나오도록
        else:
            singer.append(s.text.strip())

    for a in parse_albums:
        album.append(a.text.strip())

    # print("T", title)
    # print("S", singer)
    # print("A", album)
    path = "C:/It's_time"
    if not os.path.isdir(path):
        os.mkdir(path)
    csvfile = open("C:/It's_time/Bugs_Playlist.csv", "w", encoding='UTF-8')
    csvwriter = csv.writer(csvfile, delimiter='\\')

    for i in range(len(title)):
        #print('%3d번: %s [%s] - %s' % (i + 1, title[i], album[i], singer[i]))
        Mdg.objects.create(song=title[i], album=album[i], artist=singer[i], user_num=user, site_code='B')
        csvwriter.writerow([title[i], singer[i]])

    csvfile.close()

def get_from_vibe(id, password, user, driver):
    driver.get('https://vibe.naver.com')
    driver.find_element_by_xpath('//*[@id="app"]/div[2]/div/div/a').click() # 팝업창 닫기
    driver.find_element_by_xpath('//*[@id="app"]/div/header/div[2]/div[1]/a').click()
    #id = '' # 여기에 아이디 입력
    #pw = '' # 여기에 비밀번호
    copy_input('//*[@id="id"]', id, driver)
    copy_input('//*[@id="pw"]', password, driver)
    driver.find_element_by_xpath('//*[@id="log.login"]').click()
    driver.find_element_by_xpath('//*[@id="new.dontsave"]').click()
    # 네이버는 로그인 속도가 너무 빠르면 캡차 요구, 파이썬으로 클립보드 사용하는 방식 이용
    time.sleep(1.5)

    driver.find_element_by_xpath('//*[@id="app"]/div/header/div[2]/div[2]/div[2]/ul/li[7]/ul/li[5]/a').click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/ul/li[2]/div/div[2]/a').click() # li[2]로 수정
    time.sleep(1)

    html = driver.page_source
    parse = BeautifulSoup(html, 'html.parser')

    parse_titles = parse.find_all("td", {"class": "song"})
    parse_singers = parse.find_all("td", {"class": "artist"})
    parse_albums = parse.find_all("td", {"class": "album"})

    # print(parse_singers)
    title = []
    singer = []
    album = []

    for t in parse_titles:
        title.append(t.find('a').text)  # 양쪽 공백 제거

    for s in parse_singers:
        #try:
        #    singer.append(s.find('a', {"class": 'link_artist'}).text)
        #except AttributeError:
        #    singer.append('Various Artists')
    #     Various Artists 일때 a tag가 없어서 NoneType 요류 발생!
        singer.append(s.text.strip())

    for a in parse_albums:
        album.append(a.find('a').text)

    # print("T", title)
    # print("S", singer)
    # print("A", album)
    path = "C:/It's_time"
    if not os.path.isdir(path):
        os.mkdir(path)
    csvfile = open("C:/It's_time/VIBE_Playlist.csv", "w", encoding='UTF-8')
    csvwriter = csv.writer(csvfile, delimiter='\\')

    for i in range(len(title)):
        #print('%3d번: %s [%s] - %s' % (i + 1, title[i], album[i], singer[i]))
        Mdg.objects.create(song=title[i], album=album[i], artist=singer[i], user_num=user, site_code='V')
        csvwriter.writerow([title[i], singer[i]])

    csvfile.close()


def copy_input(xpath, input, driver):
    pyperclip.copy(input)
    driver.find_element_by_xpath(xpath).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(0.5)
