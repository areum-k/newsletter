import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. 아까 받은 열쇠(JSON) 파일 이름
key_file = 'service_account.json'

# 2. 파이썬에게 구글 드라이브/시트 권한을 줍니다
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# 3. 열쇠를 사용해서 구글에 접속합니다
creds = ServiceAccountCredentials.from_json_keyfile_name(key_file, scope)
client = gspread.authorize(creds)

# 4. 'newsletter_data' 라는 이름의 엑셀 파일을 엽니다
# (주의: 구글 시트 파일 이름이 정확해야 합니다!)
doc = client.open("newsletter_data")
sheet = doc.sheet1  # 첫 번째 시트 선택

# 5. 모든 내용을 가져와서 화면에 보여줍니다
data = sheet.get_all_records()
print("🎉 성공! 구글 시트에서 가져온 데이터:")
print(data)