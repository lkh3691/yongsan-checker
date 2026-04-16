import requests
import os
import sys

# 감시할 페이지 목록
PROGRAMS = {
    "오전반": "https://makeinyongsan.kr/program/view/69c24195847d148cf20ca6c1",
    "오후반": "https://makeinyongsan.kr/program/view/69c24207847d148cf20ca80a"
}

# 숫자를 요청할 내부 주소
API_URL = "https://makeinyongsan.kr/program/getProgramView"

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def get_count(program_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': f'https://makeinyongsan.kr/program/view/{program_id}',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        # 1차 시도: 데이터 요청
        data = {'program_idx': program_id}
        response = requests.post(API_URL, headers=headers, data=data, timeout=15)
        
        if "현재 참여" in response.text:
            idx = response.text.find("현재 참여")
            area = response.text[idx:idx+30]
            return "".join(filter(str.isdigit, area))
        
        # 2차 시도: 페이지 전체에서 찾기
        full_res = requests.get(f"https://makeinyongsan.kr/program/view/{program_id}", headers=headers, timeout=15)
        if "현재 참여" in full_res.text:
            idx = full_res.text.find("현재 참여")
            area = full_res.text[idx:idx+30]
            return "".join(filter(str.isdigit, area))

        return None
    except:
        return None

def send_telegram(msg):
    if TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

# 실행
any_success = False
for name, url in PROGRAMS.items():
    p_id = url.split('/')[-1]
    count = get_count(p_id)
    
    if count:
        any_success = True
        file_path = f"last_count_{name}.txt"
        
        # 이전 기록 읽기
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                last_count = f.read().strip()
        else:
            last_count = ""
            
        # 인원 변동 시 알림
        if count != last_count:
            send_telegram(f"📢 [{name}] 인원 변동! 현재 {count}명\n주소: {url}")
            with open(file_path, "w") as f:
                f.write(count)
    else:
        print(f"{name} 데이터를 읽어오는 데 실패했습니다.")

# 모든 페이지 실패 시 에러 종료 (로그 확인용)
if not any_success:
    sys.exit(1)
