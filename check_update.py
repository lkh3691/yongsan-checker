import requests
import os
import sys

# 웹사이트 내부 데이터 경로 (API)
PROGRAMS = {
    "오전반": "https://makeinyongsan.kr/program/view/69c24195847d148cf20ca6c1",
    "오후반": "https://makeinyongsan.kr/program/view/69c24207847d148cf20ca80a"
}

# 숫자를 뽑아내기 위한 API 주소 (추정)
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
        # 해당 사이트는 POST 방식으로 데이터를 요청할 확률이 높습니다.
        data = {'program_idx': program_id}
        response = requests.post(API_URL, headers=headers, data=data, timeout=15)
        
        # 만약 JSON 형태라면 숫자를 바로 찾고, 아니면 텍스트에서 찾습니다.
        res_text = response.text
        if "현재 참여" in res_text:
            # "현재 참여 6명" 주변에서 숫자만 추출
            start_idx = res_text.find("현재 참여")
            search_area = res_text[start_idx:start_idx+30]
            count = "".join(filter(str.isdigit, search_area))
            return count
        
        # 텍스트가 안 보일 경우 HTML 전체에서 다시 시도
        full_res = requests.get(f"https://makeinyongsan.kr/program/view/{program_id}", headers=headers)
        if "현재 참여" in full_res.text:
            idx = full_res.text.find("현재 참여")
            count = "".join(filter(str.isdigit, full_res.text[idx:idx+30]))
            return count

        return None
    except:
        return None

def send_telegram(msg):
    if TOKEN and CHAT_ID:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg})

success = False
# URL의 마지막 부분이 ID입니다. (69c24195847d148cf20ca6c1 등)
for name, url in PROGRAMS.items():
    p_id = url.split('/')[-1]
    count = get_count(p_id)
    
    if count:
        success = True
        path = f"last_count_{name}.txt"
        last = open(path, "r").read().strip() if os.path.exists(path) else ""
        
        if count != last:
            send_telegram(f"📢 [{name}] 인원 변동! 현재 {count}명\n링크: {url}")
            with open(path, "w") as f: f.write(count)
    else:
        print(f"{name} 데이터를 여전히 읽지 못함")

if not success:
    sys.exit(1)import requests
import os
import sys

# 웹사이트 내부 데이터 경로 (API)
PROGRAMS = {
    "오전반": "https://makeinyongsan.kr/program/view/69c24195847d148cf20ca6c1",
    "오후반": "https://makeinyongsan.kr/program/view/69c24207847d148cf20ca80a"
}

# 숫자를 뽑아내기 위한 API 주소 (추정)
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
        # 해당 사이트는 POST 방식으로 데이터를 요청할 확률이 높습니다.
        data = {'program_idx': program_id}
        response = requests.post(API_URL, headers=headers, data=data, timeout=15)
        
        # 만약 JSON 형태라면 숫자를 바로 찾고, 아니면 텍스트에서 찾습니다.
        res_text = response.text
        if "현재 참여" in res_text:
            # "현재 참여 6명" 주변에서 숫자만 추출
            start_idx = res_text.find("현재 참여")
            search_area = res_text[start_idx:start_idx+30]
            count = "".join(filter(str.isdigit, search_area))
            return count
        
        # 텍스트가 안 보일 경우 HTML 전체에서 다시 시도
        full_res = requests.get(f"https://makeinyongsan.kr/program/view/{program_id}", headers=headers)
        if "현재 참여" in full_res.text:
            idx = full_res.text.find("현재 참여")
            count = "".join(filter(str.isdigit, full_res.text[idx:idx+30]))
            return count

        return None
    except:
        return None

def send_telegram(msg):
    if TOKEN and CHAT_ID:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg})

success = False
# URL의 마지막 부분이 ID입니다. (69c24195847d148cf20ca6c1 등)
for name, url in PROGRAMS.items():
    p_id = url.split('/')[-1]
    count = get_count(p_id)
    
    if count:
        success = True
        path = f"last_count_{name}.txt"
        last = open(path, "r").read().strip() if os.path.exists(path) else ""
        
        if count != last:
            send_telegram(f"📢 [{name}] 인원 변동! 현재 {count}명\n링크: {url}")
            with open(path, "w") as f: f.write(count)
    else:
        print(f"{name} 데이터를 여전히 읽지 못함")

if not success:
    sys.exit(1)
