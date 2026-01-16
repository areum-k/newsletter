import gspread
from oauth2client.service_account import ServiceAccountCredentials
from jinja2 import Environment, FileSystemLoader
import shutil # 파일 복사를 위한 도구

# 1. 구글 시트 연결
key_file = 'service_account.json'
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(key_file, scope)
client = gspread.authorize(creds)

doc = client.open("newsletter_data")
sheet = doc.sheet1
data_list = sheet.get_all_records() # 모든 데이터 가져오기

print(f"✅ 총 {len(data_list)}개의 뉴스레터 데이터를 가져왔습니다.")

# 2. 템플릿 준비
file_loader = FileSystemLoader('.')
env = Environment(loader=file_loader)
template = env.get_template('template.html')

# 3. 하나씩 다 만들기 (Loop)
# 리스트를 돌면서 파일(letter_1.html, letter_2.html...)을 모두 만듭니다.
for data in data_list:
    # 템플릿에 '현재 데이터(data)'와 '전체 리스트(data_list)'를 같이 넘깁니다.
    # (그래야 하단에 '지난 글 목록'을 만들 수 있으니까요!)
    output_html = template.render(data, all_letters=data_list)
    
    # 파일명 예시: letter_1.html, letter_2.html
    filename = f"letter_{data['id']}.html"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output_html)
    
    print(f"🔨 {filename} 제작 완료!")

# 4. 가장 최신 글(맨 마지막 데이터)을 index.html(대문)로 만들기
latest_data = data_list[-1] # 리스트의 맨 마지막 요소
latest_html = template.render(latest_data, all_letters=data_list)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(latest_html)

print("🎉 모든 작업 완료! index.html이 최신 글(ID: {})로 업데이트 되었습니다.".format(latest_data['id']))