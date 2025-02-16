from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup, Tag
import json
import time

#각종 경로

#타겟 URL
TARGET_URL = "https://mapleland.gg/item/1051009?lowPrice=&highPrice=2147483647&lowincDEX=10&highincDEX=10&lowincLUK=5&highincLUK=5&lowincPDD=&highincPDD=&lowincMMP=&highincMMP=&lowUpgrade=&highUpgrade=10&lowTuc=&highTuc=10&hapStatsName=&lowHapStatsValue=0&highHapStatsValue=0"

SELLING_LIST_PATH = '#content-container > div.item_itemTradeWrap__uu_cd > div.bg-components-light.dark\:bg-components-dark.rounded.p-2 > div.grid.grid-cols-1.md\:grid-cols-2.gap-2 > div:nth-child(1) > div.max-h-\[600px\].md\:h-\[900px\].overflow-y-scroll.scrollbar-thin.dark\:scrollbar-thumb-zinc-800.dark\:scrollbar-track-zinc-600'
BUY_LIST_PATH = '#content-container > div.item_itemTradeWrap__uu_cd > div.bg-components-light.dark\:bg-components-dark.rounded.p-2 > div.grid.grid-cols-1.md\:grid-cols-2.gap-2 > div:nth-child(2) > div.max-h-\[600px\].md\:h-\[900px\].overflow-y-scroll.scrollbar-thin.dark\:scrollbar-thumb-zinc-800.dark\:scrollbar-track-zinc-600'

BUYD_CLASS = 'rounded p-2 mb-2 bg-zinc-800/20 text-gray-500'
SELLING_CLASS = 'rounded p-2 mb-2 bg-gray-300 text-zinc-700 dark:bg-zinc-800 dark:text-gray-200'

ITEM_STATUS_PATH = ''
ITEM_SPEC_PATH = 'div.flex.items-center.gap-2 > div.flex-auto.px-1 > div.text-xs.flex.justify-between > div' # 공+ 11 같은거
ITEM_NAME_PATH = 'div.flex.items-center.gap-2 > div.flex-auto.px-1 > div.flex.justify-between.items-center.font-bold.py-0\.5 > div' # 아이템 이름
ITEM_USER_URL_PATH = 'div.flex.justify-between.border-t.border-black\/10.dark\:border-white\/10.pt-1.text-xs.font-normal > a' # 거래 URL
ITEM_USER_NAME_PATH = 'div.flex.items-center.gap-2 > div.flex-auto.px-1 > div.flex.justify-between.items-center.font-bold.py-0\.5 > a > span.text-xs.truncate.w-16.text-right' #유저 이름
ITEM_PRICE_PATH = 'div.flex.items-center.gap-2 > div.flex-auto.px-1 > div.text-sm.border-t.border-black\/10.dark\:border-white\/10 > div > div' #가격(div태그까지만)
ITEM_POSTED_PATH = 'div.flex.items-center.gap-2 > div.flex-auto.px-1 > div.text-sm.border-t.border-black\/10.dark\:border-white\/10 > div > span'
ITEM_CAPTION_PATH = 'div.flex.justify-between.border-t.border-black\/10.dark\:border-white\/10.pt-1.text-xs.font-normal > div > div.hidden.md\:inline-block > button > span'

# Chrome 옵션 설정  (SSL 오류 방지)
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
options.add_argument("--ignore-certificate-errors")  # SSL 인증서 오류 무시
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--ignore-ssl-errors")  # 추가적인 SSL 오류 무시
options.add_argument("--disable-web-security")  # 웹 보안 무시
options.add_argument("--allow-running-insecure-content")  # 보안 경고 무시
options.add_argument("--no-proxy-server")  # 프록시 사용 안 함
options.add_argument("--proxy-server='direct://'")  # 직접 연결 사용

# # WebDriver 실행
print("WebDriver 실행됨")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# 웹사이트 접속
driver.get(TARGET_URL)

# JavaScript가 실행될 시간을 기다림
time.sleep(3)

# JavaScript 실행 후 HTML 가져오기
html = driver.page_source #Text 반환

#Driver 닫아주기
driver.quit()

# TEST HTML 파일 불러오기
# with open("test_page.html", "r", encoding="utf-8") as file:
#     html = file.read()  # 보기 좋은 형태로 저장

#HTML 파싱(Soup객체로)
soup = BeautifulSoup(html, "html.parser")

#목록 가져오기
items = soup.select_one(SELLING_LIST_PATH)

print(f"등록글 총 갯수: {len(items)}")

#공백 제거하기
items = [item for item in items if isinstance(item, Tag)]

ItemsList = []

# 요소들 파싱하기
for item in items :

    """ ========== 데이터 추출하기 ========== """

    # 거래 상태 클래스 추출
    itemStatusClass = " ".join(item.get("class", [])) 
    
    # 거래상태 설정하기
    if itemStatusClass == BUYD_CLASS:
        itemStatus = "팔림"
    elif itemStatusClass == SELLING_CLASS:
        itemStatus = "파는 중"
    else:
        itemStatus = "??여기 클래스 바뀐듯.."

    # 스펙
    specElements = item.select_one(ITEM_SPEC_PATH).find_all("span")
    spec = [span.text.strip() for span in specElements]

    # 아이템 이름
    itemName = item.select_one(ITEM_NAME_PATH).text.strip()  

    # 판매자 닉네임
    seller = item.select_one(ITEM_USER_NAME_PATH).text.strip()

    # 가격
    price = item.select_one(ITEM_PRICE_PATH).text.strip().split("\n")[0]

    # 등록 시간
    timePosted = item.select_one(ITEM_POSTED_PATH).text.strip()

    # 설명 추출
    descElements = item.select_one(ITEM_CAPTION_PATH)

    if descElements:
        description = descElements.text.strip()
    else:
        description = ""

    # 거래 링크
    trade_link = soup.select_one(ITEM_USER_URL_PATH)["href"]

    # JSON 형식으로 정리
    item_data = {
        "거래 상태" : itemStatus,
        "아이템 이름": itemName,
        "스펙": spec,
        "판매자": seller,
        "가격": price,
        "등록 시간": timePosted,
        "설명": description,
        "거래 링크": f"https://mapleland.gg{trade_link}"  # 상대 경로를 절대 경로로 변환
    }
    
    ItemsList.append(item_data)

# 각 항목 순회
for item in ItemsList:
    print(json.dumps(item, indent=4, ensure_ascii=False)) # 출력하기


    # print(f"회차 : {index}, 내용물 : {item} \n")