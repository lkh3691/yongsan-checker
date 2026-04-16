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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        # HTML 분석
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 방법 1: '현재 참여' 텍스트를 포함한 태그 찾기
        target = soup.find(lambda tag: tag.name in ['span', 'div', 'p', 'li'] and "현재 참여" in tag.text)
        
        if target:
            text_content = target.text.strip()
            # 숫자만 추출
            count = "".join(filter(str.isdigit, text_content))
            return count
        
        # 방법 2: 전체 텍스트에서 검색 (최후의 수단)
        full_text = soup.get_text()
        if "현재 참여" in full_text:
            start_idx = full_text.find("현재 참여")
            # 해당 문구 주변 20글자만 가져와서 숫자 추출
            sub_text = full_text[start_idx : start_idx + 20]
            count = "".join(filter(str.isdigit, sub_text))
            return count

        return None
    except Exception as e:
        print(f"접속 에러: {e}")
        return "ERROR"

def send_telegram(message):
    if not TOKEN or not CHAT_ID: return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})

# 메인 로직
any_success = False
for name, url in PROGRAMS.items():
    current_count = get_current_count(url)
    
    if current_count == "ERROR":
        continue # 접속 실패는 건너뜀

    if current_count:
        any_success = True
        file_path = f"last_count_{name}.txt"
        
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                last_count = f.read().strip()
        else:
            last_count = ""

        if current_count != last_count:
            send_telegram(f"📢 [{name}] 상태 변경!\n현재: {current_count}명 참여 중\n링크: {url}")
            with open(file_path, "w") as f:
                f.write(current_count)
    else:
        # 텔레그램으로 무엇이 문제인지 알림 (한 번만 확인용)
        print(f"{name}: '현재 참여' 문구를 찾지 못함")

# 만약 아무 데이터도 못 가져오면 강제 에러 발생 (로그 확인용)
if not any_success:
    sys.exit(1)
