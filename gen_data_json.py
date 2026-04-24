import os
import json
import re

original_dir = 'audios/original'
converted_dir = 'audios/converted'

# Lấy danh sách file gốc
original_files = [f for f in os.listdir(original_dir) if f.endswith('.wav')]
data = []

# Lấy danh sách file trong converted
converted_files = [f for f in os.listdir(converted_dir) if f.endswith('.wav')]

for f in original_files:
    name_no_ext = os.path.splitext(f)[0]

    # Tạo pattern để tìm các file liên quan:
    # Khớp chính xác "ID.wav" hoặc "ID_hậu_tố.wav"
    # Ví dụ với ID là 1: khớp "1.wav", "1_male.wav", "1_male_1.wav"
    # Không khớp: "10.wav", "11.wav"
    pattern = re.compile(rf"^{re.escape(name_no_ext)}(_.*)?\.wav$")

    related_files = [cf for cf in converted_files if pattern.match(cf)]

    female_file = f if f in related_files else None

    male_file_name = f"{name_no_ext}_male.wav"
    male_path = f"audios/converted/{male_file_name}" if male_file_name in related_files else None

    # Tìm các file "others" (có trong related nhưng không phải female và không phải male chuẩn)
    others = []
    for cf in related_files:
        if cf != f and cf != male_file_name:
            others.append(f"audios/converted/{cf}")

    data.append({
        "id": name_no_ext,
        "original": f"audios/original/{f}",
        "female": f"audios/converted/{f}" if female_file else None,
        "male": male_path,
        "others": sorted(others)
    })

# Sắp xếp lại data theo ID số (nếu ID là số) để hiển thị đúng thứ tự 1, 2, 3... thay vì 1, 10, 11
try:
    data.sort(key=lambda x: int(x['id']))
except ValueError:
    data.sort(key=lambda x: x['id'])

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Đã cập nhật data.json thành công.")