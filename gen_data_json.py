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
    # 1. Lấy tên file bỏ đuôi .wav
    full_name = os.path.splitext(f)[0]

    # 2. Loại bỏ hậu tố "_original" để lấy ID thực tế
    # Ví dụ: "1_original" -> "1", "song_abc_original" -> "song_abc"
    name_no_ext = re.sub(r'_original$', '', full_name)

    # 3. Pattern tìm kiếm: Khớp với ID hoặc ID_hậu_tố
    # Logic: Tìm các file trong converted bắt đầu bằng ID, theo sau là dấu gạch dưới hoặc kết thúc luôn
    pattern = re.compile(rf"^{re.escape(name_no_ext)}(_.*)?\.wav$")
    related_files = [cf for cf in converted_files if pattern.match(cf)]

    # 4. Xác định file female (thường trùng tên với ID ban đầu hoặc giữ nguyên file gốc)
    # Tùy vào việc folder converted của bạn lưu file nữ là "1.wav" hay "1_original.wav"
    # Ở đây mình ưu tiên tìm file "ID.wav" trước
    female_file_name = f"{name_no_ext}.wav"
    female_path = f"audios/converted/{female_file_name}" if female_file_name in related_files else None

    # 5. Xác định file male chuẩn (ID_male.wav)
    male_file_name = f"{name_no_ext}_male.wav"
    male_path = f"audios/converted/{male_file_name}" if male_file_name in related_files else None

    # 6. Tìm các file "others"
    # Loại trừ file male_file_name và female_file_name đã xác định ở trên
    others = []
    for cf in related_files:
        if cf != female_file_name and cf != male_file_name:
            others.append(f"audios/converted/{cf}")

    data.append({
        "id": name_no_ext,
        "original": f"audios/original/{f}",
        "female": female_path,
        "male": male_path,
        "others": sorted(others)
    })

# Sắp xếp lại data theo ID
try:
    data.sort(key=lambda x: int(x['id']))
except ValueError:
    data.sort(key=lambda x: x['id'])

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Đã cập nhật data.json thành công với ID sạch (không kèm _original).")