import gspread
from oauth2client.service_account import ServiceAccountCredentials
from jinja2 import Environment, FileSystemLoader
import os # 👈 폴더를 만들고 관리하기 위한 도구 추가

# --- 1. 구글 시트 연결 (그대로) ---
key_file = 'service_account.json'
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(key_file, scope)
client = gspread.authorize(creds)
doc = client.open("newsletter_data")
sheet = doc.sheet1
data_list = sheet.get_all_records()
print(f"✅ 총 {len(data_list)}개의 뉴스레터 데이터를 가져왔습니다.")

# --- 2. 템플릿 준비 (그대로) ---
file_loader = FileSystemLoader('.')
env = Environment(loader=file_loader)
template = env.get_template('template.html')

# --- 3. 폴더 정리 준비 (✨추가된 부분✨) ---
# 'archives' 라는 이름의 폴더가 없으면 새로 만듭니다.
output_dir = 'archives'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"📂 '{output_dir}' 폴더를 새로 만들었습니다.")

# --- 4. 하나씩 다 만들기 (Loop) ---
for data in data_list:
    # (중요!) 템플릿에 '이 파일이 저장될 폴더 이름'도 같이 알려줍니다.
    # 그래야 링크를 걸 때 'archives/letter_1.html' 처럼 경로를 알 수 있거든요.
    output_html = template.render(data, all_letters=data_list, folder_name=output_dir)
    
    # 파일 경로를 'archives/letter_id.html'로 설정합니다.
    filename = os.path.join(output_dir, f"letter_{data['id']}.html")
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output_html)
    
    print(f"🔨 {filename} 제작 완료!")

# --- 5. 최신 글 대문 만들기 (index.html) ---
latest_data = data_list[-1]
# index.html은 바깥에 저장되므로 folder_name을 비워둡니다.
latest_html = template.render(latest_data, all_letters=data_list, folder_name="")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(latest_html)

print("🎉 모든 작업 완료! archives 폴더와 index.html을 확인하세요.")