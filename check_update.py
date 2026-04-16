name: Check Attendance

on:
  schedule:
    - cron: '*/15 * * * *'
  workflow_dispatch:

jobs:
  run-bot:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          # 파이썬 패키지 캐싱
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install requests playwright

      # ⭐ 핵심: Playwright 브라우저 캐싱 설정
      - name: Cache Playwright browsers
        id: playwright-cache
        uses: actions/cache@v3
        with:
          path: ~/.cache/ms-playwright
          key: ${{ runner.os }}-playwright-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-playwright-

      # 캐시가 없을 때만 브라우저 설치
      - name: Install Playwright Browsers
        if: steps.playwright-cache.outputs.cache-hit != 'true'
        run: playwright install chromium --with-deps

      # 캐시가 있어도 필요한 시스템 의존성만 설치 (매우 빠름)
      - name: Install Playwright system dependencies
        if: steps.playwright-cache.outputs.cache-hit == 'true'
        run: playwright install-deps chromium

      - name: Run script
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python check_update.py

      - name: Update record
        run: |
          git config --global user.name 'github-actions[bot]'
          git config --global user.email 'github-actions[bot]@users.noreply.github.com'
          git add last_count_*.txt
          git commit -m "Update counts" || exit 0
          git push
