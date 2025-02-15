from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

#상수부

TARGET_URL = "https://mapleland.gg/item/1442015?lowPrice=&highPrice=2147483647&lowincPAD=65&highincPAD=65&lowUpgrade=&highUpgrade=7&lowTuc=&highTuc=7"
SERCH_TYPE = "팝니다"
#Xpath 예시 
#//*[@id="content-container"]/div[2]/div[3]/div[3]/div[1]/div[2]/div[{여기서부터 항목번호}]/div[1]/div[2]/div[1]/div/span
#//*[@id="content-container"]/div[2]/div[3]/div[3]/div[{#팝니다 1,삽니다 2}]/div[2]//


# Chrome 옵션 설정
options = Options()
options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# WebDriver 실행
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 웹사이트 접속
driver.get(TARGET_URL)

# JavaScript가 실행될 시간을 기다림
time.sleep(1)

# JavaScript 실행 후 HTML 가져오기
html = driver.page_source #Text 반환

#Driver 닫아주기
driver.quit()

#HTML 파싱(Soup객체로)
soup = BeautifulSoup(html, "lxml")

#해당 태그에 있는 팝니다, 삽니다 모두 
category_div = soup.find("div",string=SERCH_TYPE).find_next_sibling()


#HTML 찾기
print("category_div: ", category_div)



