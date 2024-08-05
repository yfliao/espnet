import os
import json
import re
from zhon.hanzi import punctuation
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

def remove_invalid_tailo(text):
    # 定义台罗拼音的正则表达式模式，只保留台罗拼音中的符号
    valid_tailo_pattern = re.compile(r'[^aáàâǎa̋āa̍beéèêěe̋ēe̍ghiíìîǐi̋īi̍klmḿm̀m̂m̌m̋m̄m̍nńǹn̂ňn̋n̄n̍oóòôǒőōo̍prstuúùûǔűūu̍\- ]')
    # 使用正则表达式替换不正确的台罗拼音符号
    cleaned_text = valid_tailo_pattern.sub('', text)
    return cleaned_text

# Function to remove digits from 台羅數字調
def remove_tones(text):
    text = re.sub(r'[\d]', '', text.lower())
    text = re.sub(r'[-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Replace punctuation with space and remove duplicate spaces
def clean_text_hanlo(text):
    text = re.sub(r'[%s]+'% punctuation, ' ', text.lower())
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Replace punctuation with space and remove duplicate spaces
def clean_text_tailo(text):
    text = re.sub(r'[%s]+'% punctuation, ' ', text.lower())
    text = remove_invalid_tailo(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Replace punctuation with space and remove duplicate spaces
def clean_text_tailo_numbered(text):
    text = re.sub(r'[^a-z0-9\s-]', ' ', text.lower())
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Main function to process the JSON files
def process_json_files(directory, subset):
    json_files = find_json_files(directory+'/'+subset)
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

        ID = parts[4] + "_" + parts[5]
        ID = ID.replace('.json','')
        filepath = json_file

        hanlo = data.get("漢羅台文", "")
        tailo = data.get("台羅", "")
        tailo_numbered = data.get("台羅數字調", "")

        hanlo = clean_text_hanlo(hanlo)
        tailo = clean_text_tailo(tailo)
        tailo_numbered = clean_text_tailo_numbered(tailo_numbered)
        tailo_toneless = remove_tones(tailo_numbered)

        print(f"{filepath}")
        print(f"{subset} {ID} 漢羅台文: {hanlo}")
        print(f"{subset} {ID} 台羅: {tailo}")
        print(f"{subset} {ID} 台羅數字調: {tailo_numbered}")
        print(f"{subset} {ID} 台羅數字調無聲調: {tailo_toneless}")

        hanlo_lines.append(f"{ID} {hanlo}\n")
        tailo_lines.append(f"{ID} {tailo}\n")
        tailo_tone_lines.append(f"{ID} {tailo_numbered}\n")
        tailo_toneless_lines.append(f"{ID} {tailo_toneless}\n")

    with open("data/"+subset.lower()+'/'+'hanlo.txt', 'w', encoding='utf-8') as f:
        f.writelines(hanlo_lines)
    
    with open("data/"+subset.lower()+'/'+'tailo.txt', 'w', encoding='utf-8') as f:
        f.writelines(tailo_lines)
    
    with open("data/"+subset.lower()+'/'+'tailo-tone.txt', 'w', encoding='utf-8') as f:
        f.writelines(tailo_tone_lines)
    
    with open("data/"+subset.lower()+'/'+'tailo-toneless.txt', 'w', encoding='utf-8') as f:
        f.writelines(tailo_toneless_lines)

# Example usage
process_json_files('downloads/TAT-MOE-Lavalier','Train')
process_json_files('downloads/TAT-MOE-Lavalier','Eval')
process_json_files('downloads/TAT-MOE-Lavalier','Test')
