import requests
from bs4 import BeautifulSoup
import os

# 감시할 페이지 목록
PROGRAMS = {
    "오전반": "https://makeinyongsan.kr/program/view/69c24195847d148cf20ca6c1",
    "오후반": "https://makeinyongsan.kr/program/view/69c24207847d148cf20ca80a"
}

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def get_current_count(url):
    try:
        # 웹페이지 HTML 가져오기
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # '현재 참여 6명' 문구가 포함된 요소 찾기
        element = soup.find(text=lambda t: "현재 참여" in t)
        if element:
            # 숫자만 추출 (예: '6')
            count = "".join(filter(str.isdigit, element))
            return count
    except Exception as e:
        print(f"에러 발생 ({url}): {e}")
    return None

def send_telegram(message):
    if not TOKEN or not CHAT_ID:
        print("토큰 또는 채팅 ID가 설정되지 않았습니다.")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")

for name, url in PROGRAMS.items():
    current_count = get_current_count(url)
    file_path = f"last_count_{name}.txt"

    if current_count:
        # 이전 기록 읽기
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                last_count = f.read().strip()
        else:
            last_count = ""

        # 숫자가 바뀌었는지 확인 (빈자리가 나면 알림)
        if current_count != last_count:
            status = "인원 변동 발생!"
            message = f"📢 [{name}] {status}\n현재 참여 인원: {current_count}명\n링크: {url}"
            send_telegram(message)
            
            # 새로운 숫자 저장
            with open(file_path, "w") as f:
                f.write(current_count)
    else:
        print(f"{name} 데이터를 가져오는 데 실패했습니다.")import requests
from bs4 import BeautifulSoup
import os

# 감시할 페이지 목록
PROGRAMS = {
    "오전반": "https://makeinyongsan.kr/program/view/69c24195847d148cf20ca6c1",
    "오후반": "https://makeinyongsan.kr/program/view/69c24207847d148cf20ca80a"
}

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def get_current_count(url):
    try:
        # 웹페이지 HTML 가져오기
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # '현재 참여 6명' 문구가 포함된 요소 찾기
        element = soup.find(text=lambda t: "현재 참여" in t)
        if element:
            # 숫자만 추출 (예: '6')
            count = "".join(filter(str.isdigit, element))
            return count
    except Exception as e:
        print(f"에러 발생 ({url}): {e}")
    return None

def send_telegram(message):
    if not TOKEN or not CHAT_ID:
        print("토큰 또는 채팅 ID가 설정되지 않았습니다.")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")

for name, url in PROGRAMS.items():
    current_count = get_current_count(url)
    file_path = f"last_count_{name}.txt"

    if current_count:
        # 이전 기록 읽기
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                last_count = f.read().strip()
        else:
            last_count = ""

        # 숫자가 바뀌었는지 확인 (빈자리가 나면 알림)
        if current_count != last_count:
            status = "인원 변동 발생!"
            message = f"📢 [{name}] {status}\n현재 참여 인원: {current_count}명\n링크: {url}"
            send_telegram(message)
            
            # 새로운 숫자 저장
            with open(file_path, "w") as f:
                f.write(current_count)
    else:
        print(f"{name} 데이터를 가져오는 데 실패했습니다.")
