from playwright.sync_api import sync_playwright
import os
import requests
import re

# 감시할 설정
PROGRAMS = {
    "오전반": "69c24195847d148cf20ca6c1",
    "오후반": "69c24207847d148cf20ca80a"
}
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_count(p_idx):
    url = f"https://makeinyongsan.kr/program/view/{p_idx}"
    try:
        with sync_playwright() as p:
            # 브라우저 실행
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            # 화면이 다 그려질 때까지 3초 대기
            page.wait_for_timeout(3000)
            content = page.content()
            browser.close()

            # "현재 참여 6명" 문구에서 숫자 추출
            match = re.search(r"현재 참여\s*(\d+)명", content)
            return match.group(1) if match else None
    except Exception as e:
        print(f"에러 발생 ({p_idx}): {e}")
        return None

def send_telegram(message):
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})

# 메인 실행 반복문
for name, p_idx in PROGRAMS.items():
    current = get_count(p_idx)
    
    if current:
        file_path = f"last_count_{name}.txt"
        
        # 이전 숫자 읽기
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                last = f.read().strip()
        else:
            last = ""
        
        # 숫자가 바뀌었을 때만 알림
        if current != last:
            msg = f"📢 [{name}] 인원 변동 감지!\n현재 인원: {current}명\n링크: https://makeinyongsan.kr/program/view/{p_idx}"
            send_telegram(msg)
            
            # 새로운 숫자 저장
            with open(file_path, "w") as f:
                f.write(current)
    else:
        print(f"{name} 정보를 읽지 못했습니다.")
