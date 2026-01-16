import pandas as pd
import json
import re

# Tên file của bạn
input_file = 'danhsachquaythuong.csv'
output_file = 'member1.js'

def xoa_tieng_trung(text):
    if isinstance(text, str):
        # Regex xóa các ký tự trong phạm vi Unicode chữ Hán
        return re.sub(r'[\u4e00-\u9fff]', '', text).strip()
    return text

try:
    # Đọc file CSV (chú ý encoding='utf-8-sig' để đọc tốt tiếng Việt)
    # sep=';' vì file của bạn ngăn cách bằng dấu chấm phẩy
    # skiprows=1 để bỏ qua dòng tiêu đề bị lỗi đầu tiên
    df = pd.read_csv(input_file, sep=';', header=None, skiprows=1, 
                     names=['phone', 'name'], encoding='utf-8-sig', on_bad_lines='skip')

    # Bước 1: Xóa tiếng Trung trong cột 'name'
    df['name'] = df['name'].apply(xoa_tieng_trung)

    # Bước 2: Chuyển dữ liệu sang dạng Dictionary
    data = df.to_dict(orient='records')

    # Bước 3: Tạo chuỗi định dạng JS
    js_content = "var member = " + json.dumps(data, ensure_ascii=False, indent=2) + ";"

    # Lưu ra file .js
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"Đã tạo xong file: {output_file}")

except Exception as e:
    print(f"Lỗi: {e}")