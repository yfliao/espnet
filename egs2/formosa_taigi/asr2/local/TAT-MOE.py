import os, sys
import json
import re
import string
from zhon.hanzi import punctuation
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音

def remove_punctuation_except_hyphen(text):
    # Define the Tailo characters
    tailo_chars = 'aáàâǎa̋āa̍beéèêěe̋ēe̍ghiíìîǐi̋īi̍klmḿm̀m̂m̌m̋m̄m̍nńǹn̂ňn̋n̄n̍oóòôǒőōo̍prstuúùûǔűūu̍'
    tailo_chars_set = set(tailo_chars)

    # Remove all punctuation except dashes
    text = re.sub(r'[^\w\s{}-]'.format(re.escape(tailo_chars)), '', text)

    # Function to remove incorrectly placed dashes
    def correct_dashes(text):
        result = []
        i = 0
        while i < len(text):
            if text[i] == '-' and i + 1 < len(text) and text[i + 1] == '-':
                # Handle double dash
                if (i > 0 and text[i - 1] in tailo_chars_set and i + 2 < len(text) and text[i + 2] in tailo_chars_set) or \
                   (i > 0 and i + 2 < len(text) and text[i + 2] in tailo_chars_set) or \
                   (i == 0 and i + 2 < len(text) and text[i + 2] in tailo_chars_set):
                    result.append('--')
                    i += 2
                else:
                    i += 2
            elif text[i] == '-':
                # Handle single dash
                if i > 0 and text[i - 1] in tailo_chars_set and i + 1 < len(text) and text[i + 1] in tailo_chars_set:
                    result.append('-')
                i += 1
            else:
                result.append(text[i])
                i += 1
        return ''.join(result)

    # Apply dash correction
    text = correct_dashes(text)

    return text

def remove_spaces_between_cjk(text):
    # Regular expression to match spaces between CJK characters
    pattern = re.compile(r'(?<=[\u4e00-\u9fff]) (?=[\u4e00-\u9fff])')
    # Replace the matched spaces with an empty string
    result = re.sub(pattern, '', text)
    return result

def remove_spaces_between_cjk_and_tailo(text):
    # Define the set of Tailo characters as a string for regex matching
    tailo_chars = 'aáàâǎa̋āa̍beéèêěe̋ēe̍ghiíìîǐi̋īi̍klmḿm̀m̂m̌m̋m̄m̍nńǹn̂ňn̋n̄n̍oóòôǒőōo̍prstuúùûǔűūu̍'
    tailo_pattern = f'a-z{re.escape(tailo_chars)}'

    # Define CJK Unicode range
    cjk_pattern = '\u4E00-\u9FFF'

    # Compile the regex patterns for removing spaces
    pattern1 = re.compile(f'([{tailo_pattern}])\s+([{cjk_pattern}])')
    pattern2 = re.compile(f'([{cjk_pattern}])\s+([{tailo_pattern}])')
    pattern3 = re.compile(f'([{cjk_pattern}])\s+([{cjk_pattern}])')

    # Remove spaces between Tailo characters/a-z and CJK characters
    text = pattern1.sub(r'\1\2', text)
    text = pattern2.sub(r'\1\2', text)
    text = pattern3.sub(r'\1\2', text)
    return text

def remove_invalid_tailo(text):
    # 定义台罗拼音的正则表达式模式，只保留台罗拼音中的符号
    valid_tailo_pattern = re.compile(r'[^aáàâǎa̋āa̍beéèêěe̋ēe̍ghiíìîǐi̋īi̍klmḿm̀m̂m̌m̋m̄m̍nńǹn̂ňn̋n̄n̍oóòôǒőōo̍prstuúùûǔűūu̍\- ]')
    # 使用正则表达式替换不正确的台罗拼音符号
    cleaned_text = valid_tailo_pattern.sub('', text)
    return cleaned_text

# Function to remove digits from 台羅數字調
def remove_tones(text):
    text = re.sub(r'[\d]', '', text.lower())
#    text = re.sub(r'[-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Replace punctuation with space and remove duplicate spaces
def clean_text_hanlo(text):
    text = re.sub(r"[%s]+" % punctuation, ' ', text.lower())
    text = remove_punctuation_except_hyphen(text)
    text = re.sub(r'\s+', ' ', text)
    text = remove_spaces_between_cjk_and_tailo(text)
    return text.strip()

# Replace punctuation with space and remove duplicate spaces
def clean_text_tailo(text):
    text = re.sub(r"[%s]+" % punctuation, ' ', text.lower())
#    text = re.sub(r"[%s]+" % string.punctuation, ' ', text)
    text = remove_invalid_tailo(text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Replace punctuation with space and remove duplicate spaces
def clean_text_tailo_list(intext):
    text = []
    for line in intext:
        line = re.sub(r"[%s]+" % punctuation, ' ', line.lower())
        line = remove_invalid_tailo(line)
        line = re.sub(r'\s+', ' ', line)
        text.append(line)
    return text

# Replace punctuation with space and remove duplicate spaces
def clean_text_tailo_numbered(text):
    text = re.sub(r'[^a-z0-9\s-]', ' ', text.lower())
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Replace punctuation with space and remove duplicate spaces
def clean_text_en(text):
    text = re.sub(r'[^a-z0-9\s-]', ' ', text.lower())
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# remove all symbols from a text except for those used in Pe̍h-ōe-jī (POJ)
def remove_non_poj_symbols(text):
    # Define the valid POJ character set including diacritics, space, and hyphen
    valid_poj_pattern = re.compile(r"[a-zA-Zô̍̄́̀̂ṳḿńǹêîâáàûúīíì\- ]+", re.UNICODE)
    
    # Find all valid POJ sequences and join them back into a string
    filtered_text = ''.join(valid_poj_pattern.findall(text))
    
    return filtered_text

# Helper function to recursively find all JSON files in a directory
def find_json_files(directory):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    return json_files

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

        # print(f"{filepath}")
        # print(f"{subset} {ID} 漢羅台文: {hanlo}")
        # print(f"{subset} {ID} 台羅: {tailo}")
        # print(f"{subset} {ID} 台羅數字調: {tailo_numbered}")
        # print(f"{subset} {ID} 台羅數字調無聲調: {tailo_toneless}")

        hanlo_lines.append(f"{ID} {hanlo}\n")
        tailo_lines.append(f"{ID} {tailo}\n")
        tailo_tone_lines.append(f"{ID} {tailo_numbered}\n")
        tailo_toneless_lines.append(f"{ID} {tailo_toneless}\n")

    with open("data/"+subset+'/'+'hanlo.txt', 'w', encoding='utf-8') as f:
        f.writelines(hanlo_lines)
    
    with open("data/"+subset+'/'+'tailo.txt', 'w', encoding='utf-8') as f:
        f.writelines(tailo_lines)
    
    with open("data/"+subset+'/'+'tailo-tone.txt', 'w', encoding='utf-8') as f:
        f.writelines(tailo_tone_lines)
    
    with open("data/"+subset+'/'+'tailo-toneless.txt', 'w', encoding='utf-8') as f:
        f.writelines(tailo_toneless_lines)

# Example usage
os.makedirs('data/Train', exist_ok=True);
os.makedirs('data/Eval', exist_ok=True);
os.makedirs('data/Test', exist_ok=True);

process_json_files('downloads/TAT-MOE-Lavalier','Train')
process_json_files('downloads/TAT-MOE-Lavalier','Eval')
process_json_files('downloads/TAT-MOE-Lavalier','Test')
