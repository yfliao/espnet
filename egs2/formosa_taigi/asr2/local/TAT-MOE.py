import os
import json
import re
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音

# Helper function to recursively find all JSON files in a directory
def find_json_files(directory):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files

# Function to convert 台羅 to 台羅數字調
def convert_tailo_to_numbered(tailo):
    tailo_obj = 拆文分析器.建立句物件(tailo)
    return tailo_obj.轉音(臺灣閩南語羅馬字拼音).看語句()

# Function to remove digits from 台羅數字調
def remove_tones(numbered_tailo):
    return re.sub(r'\d', '', numbered_tailo)

# Replace punctuation with space and remove duplicate spaces
def clean_text(text):
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Main function to process the JSON files
def process_json_files(directory):
    json_files = find_json_files(directory)
    hanlo_lines = []
    tailo_lines = []
    tailo_tone_lines = []
    tailo_toneless_lines = []

    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        parts = json_file.split(os.sep)
        if len(parts) < 6:
            continue

        ID = parts[4] + parts[5]
        ID = ID.replace('.json','')
        filepath = json_file

        hanlo = data.get("漢羅台文", "")
        tailo = data.get("台羅", "")

        tailo_numbered = convert_tailo_to_numbered(tailo)
        tailo_toneless = remove_tones(tailo_numbered)

        hanlo = clean_text(hanlo)
        tailo = clean_text(tailo)
        tailo_numbered = clean_text(tailo_numbered)
        tailo_toneless = clean_text(tailo_toneless)

        print(f"{filepath}")
        print(f"{ID} 漢羅台文: {hanlo}")
        print(f"{ID} 台羅: {tailo}")
        print(f"{ID} 台羅數字調: {tailo_numbered}")
        print(f"{ID} 台羅數字調無聲調: {tailo_toneless}")

        hanlo_lines.append(f"{ID} {hanlo}\n")
        tailo_lines.append(f"{ID} {tailo}\n")
        tailo_tone_lines.append(f"{ID} {tailo_numbered}\n")
        tailo_toneless_lines.append(f"{ID} {tailo_toneless}\n")

    with open('hanlo.txt', 'w', encoding='utf-8') as f:
        f.writelines(hanlo_lines)
    
    with open('tailo.txt', 'w', encoding='utf-8') as f:
        f.writelines(tailo_lines)
    
    with open('tailo-tone.txt', 'w', encoding='utf-8') as f:
        f.writelines(tailo_tone_lines)
    
    with open('tailo-toneless.txt', 'w', encoding='utf-8') as f:
        f.writelines(tailo_toneless_lines)

# Example usage
process_json_files('downloads/TAT-MOE-Lavalier')
