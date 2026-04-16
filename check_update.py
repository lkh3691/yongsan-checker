import requests
from bs4 import BeautifulSoup
import os

PROGRAMS = {
    "오전반": "https://makeinyongsan.kr/program/view/69c24195847d148cf20ca6c1",
    "오후반": "https://makeinyongsan.kr/program/view/69c24207847d148cf20ca80a"
}

TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

def get_current_count(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.find(text=lambda t: "현재 참여" in t)
        if element:
            return "".join(filter(str.isdigit, element))
    except Exception as e:
        print(f"에러: {e}")
    return None

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})

for name, url in PROGRAMS.items():
    current_count = get_current_count(url)
    file_path = f"last_count_{name}.txt"
    
    if current_count:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                last_count = f.read().strip()
        else:
            last_count = ""

        if current_count != last_count:
            # 숫자가 변하면 알림 전송 (예: 6명 -> 5명 되면 바로 알림)
            send_telegram(f"📢 [{name}] 인원 변동! 현재 {current_count}명\n확인: {url}")
            with open(file_path, "w") as f:
                f.write(current_count)
