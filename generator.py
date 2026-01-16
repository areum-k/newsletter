import gspread
from oauth2client.service_account import ServiceAccountCredentials
from jinja2 import Environment, FileSystemLoader

# --- 1. 구글 시트 연결 (아까 했던 것) ---
key_file = 'service_account.json'
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(key_file, scope)
client = gspread.authorize(creds)

# 시트 열기
doc = client.open("newsletter_data")
sheet = doc.sheet1
data_list = sheet.get_all_records()

# 가장 최근 데이터(첫 번째 줄) 가져오기
latest_data = data_list[0] 
print("✅ 구글 시트 데이터 가져오기 성공:", latest_data)

# --- 2. HTML 틀(템플릿) 준비 ---
file_loader = FileSystemLoader('.') # 현재 폴더에서 파일 찾기
env = Environment(loader=file_loader)
template = env.get_template('template.html') # 껍데기 파일 불러오기

# --- 3. 데이터 주입 (렌더링) ---
# 구글 시트의 데이터(latest_data)를 HTML 구멍에 채워 넣습니다.
output_html = template.render(latest_data)

# --- 4. 완성된 파일 저장 ---
# 결과를 'index.html'이라는 이름으로 저장합니다.
with open("index.html", "w", encoding="utf-8") as f:
    f.write(output_html)

print("🎉 뉴스레터 제작 완료! 'index.html' 파일을 확인해보세요.")