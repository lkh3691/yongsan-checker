import requests
from bs4 import BeautifulSoup
import os
import sys

# 감시할 페이지 목록
PROGRAMS = {
    "오전반": "https://makeinyongsan.kr/program/view/69c24195847d148cf20ca6c1",
    "오후반": "https://makeinyongsan.kr/program/view/69c24207847d148cf20ca80a"
}

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def get_current_count(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status() # 접속 에러 시 예외 발생
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # '현재 참여' 글자를 포함한 요소를 찾음
        element = soup.find(string=lambda t: t and "현재 참여" in t)
        
        if element:
            # 숫자만 추출
            count = "".join(filter(str.isdigit, str(element)))
            return count
        else:
            print(f"로그: {url} 페이지에서 '현재 참여' 문구를 찾을 수 없습니다.")
            return None
    except Exception as e:
        print(f"로그: {url} 접속 중 에러 발생 - {e}")
        return None

def send_telegram(message):
    if not TOKEN or not CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message}, timeout=10)
    except Exception as e:
        print(f"텔레그램 전송 에러: {e}")

# 메인 실행부
success_flag = False
for name, url in PROGRAMS.items():
    current_count = get_current_count(url)
    
    if current_count:
        success_flag = True
        file_path = f"last_count_{name}.txt"
        
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                last_count = f.read().strip()
        else:
            last_count = ""

        if current_count != last_count:
            send_telegram(f"📢 [{name}] 인원 변동! 현재 {current_count}명\n확인: {url}")
            with open(file_path, "w") as f:
                f.write(current_count)
    else:
        print(f"{name} 데이터를 가져오지 못했습니다.")

# 만약 두 페이지 모두 실패했다면 에러로 종료하여 로그 남김
if not success_flag:
    print("모든 페이지의 데이터를 가져오는 데 실패했습니다.")
    sys.exit(1)
