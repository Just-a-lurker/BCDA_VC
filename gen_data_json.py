import os
import json
import re

original_dir = 'audios/original'
converted_dir = 'audios/converted'

# Lấy danh sách file gốc (ví dụ: 1_original.wav)
all_originals = [f for f in os.listdir(original_dir) if f.endswith('_original.wav')]
data = []

# Lấy danh sách file đã convert
converted_files = [f for f in os.listdir(converted_dir) if f.endswith('.wav')]

for f in all_originals:
    # Tách ID: "1_original.wav" -> "1"
    name_id = f.replace('_original.wav', '')

    # Pattern để tìm các file liên quan chính xác tới ID
    # Khớp "ID.wav" hoặc "ID_anything.wav" nhưng không khớp "ID0.wav"
    pattern = re.compile(rf"^{re.escape(name_id)}(_.*)?\.wav$")
    related = [cf for cf in converted_files if pattern.match(cf)]

    female_others = []
    male_others = []
    female_main = None
    male_main = None

    for cf in related:
        path = f"audios/converted/{cf}"
        if "_male" in cf:
            if cf == f"{name_id}_male.wav":
                male_main = path
            else:
                male_others.append(path)
        else:
            if cf == f"{name_id}.wav":
                female_main = path
            else:
                female_others.append(path)

    data.append({
        "id": name_id,
        "original": f"audios/original/{f}",
        "female_main": female_main,
        "female_others": sorted(female_others),
        "male_main": male_main,
        "male_others": sorted(male_others),
        "is_prefix_0": name_id.startswith("0_")
    })


# Sắp xếp theo ID (ưu tiên sắp xếp số nếu ID là số)
def get_sort_key(item):
    val = item['id']
    if val.startswith("0_"):
        # Tách phần sau 0_ để so sánh số
        parts = val.split('_')
        return (0, int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else parts[1])
    return (1, int(val) if val.isdigit() else val)


data.sort(key=get_sort_key)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"Thành công: Đã xử lý {len(data)} mẫu audios.")