import smtplib
import gspread
import time # 메일 보낼 때 잠깐 쉬기 위해 필요
from oauth2client.service_account import ServiceAccountCredentials
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ==========================================
# 👇 여기만 본인 정보로 수정하세요!
# ==========================================
MY_EMAIL = "love.hawaii.kim@gmail.com"        # 보내는 사람
MY_PASSWORD = "laga lwxj picx oyfp"   # 앱 비밀번호 16자리
# ==========================================

def get_subscribers():
    """구글 시트 'subscribers' 탭에서 이메일 목록을 가져옵니다."""
    print("📋 구독자 명단을 불러오는 중...")
    
    # 구글 시트 연결
    key_file = 'service_account.json'
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(key_file, scope)
    client = gspread.authorize(creds)
    
    # 'subscribers' 시트 열기
    doc = client.open("newsletter_data")
    sheet = doc.worksheet("subscribers") # 탭 이름이 subscribers 여야 합니다!
    
    # 1번째 열(A열)의 모든 데이터를 가져옵니다 (헤더 포함)
    emails = sheet.col_values(1)
    
    # 첫 번째 줄('email' 제목)은 빼고, 실제 이메일만 리스트로 만듭니다.
    real_emails = emails[1:] 
    return real_emails

def send_newsletter():
    # 1. 보낼 내용(HTML) 준비
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print("❌ index.html 파일이 없습니다. generator.py를 먼저 실행하세요!")
        return

    # 2. 구독자 리스트 가져오기
    subscribers = get_subscribers()
    print(f"👥 총 {len(subscribers)}명에게 발송을 시작합니다.")

    # 3. 지메일 서버 로그인 (한 번만 로그인해서 계속 씀)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(MY_EMAIL, MY_PASSWORD)

    # 4. 한 명씩 반복해서 보내기
    success_count = 0
    
    for email in subscribers:
        try:
            # 편지 봉투 만들기
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"📢 [뉴스레터] {datetime.now().strftime('%Y-%m-%d')} 소식입니다!"
            msg['From'] = MY_EMAIL
            msg['To'] = email
            
            # 내용 담기
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))
            
            # 발송!
            server.sendmail(MY_EMAIL, email, msg.as_string())
            print(f"✅ 발송 성공: {email}")
            success_count += 1
            
            # 너무 빨리 보내면 구글이 스팸으로 오해하니까 2초 쉽니다.
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ 발송 실패 ({email}): {e}")

    server.quit()
    print(f"🎉 발송 완료! 총 {success_count}통을 보냈습니다.")

# 실행
if __name__ == "__main__":
    send_newsletter()