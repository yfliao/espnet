import os, sys
import pandas as pd
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
    text = re.sub(r'[-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def add_space_cjk(text):
    # This regular expression will match any CJK character
    cjk_pattern = re.compile(r'([\u4E00-\u9FFF\u3400-\u4DBF\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7AF])')
    # Add spaces around each CJK character
    spaced_text = cjk_pattern.sub(r' \1 ', text)
    # Remove any extra spaces introduced at the start or end
    spaced_text = spaced_text.strip()
    # Replace multiple spaces with a single space
    spaced_text = re.sub(' +', ' ', spaced_text)
    return spaced_text


# Replace punctuation with space and remove duplicate spaces
def clean_text_hanlo_tai(intext):
    text = []
    for line in intext:
        ID, line = line.split(" ", 1)
        line = re.sub(r"[%s]+" % punctuation, ' ', line.lower())
        line = remove_punctuation_except_hyphen(line)
        line = add_space_cjk(line)        
        line = re.sub(r'-', ' ', line)
        line = re.sub(r'\s+', ' ', line)
#        line = remove_spaces_between_cjk_and_tailo(line)
        text.append(ID+" "+line.strip())
    return text

### Replace punctuation with space and remove duplicate spaces
def clean_text_tailo(intext):
    text = []
    for line in intext:
        ID, line = line.split(" ", 1)
        line = re.sub(r"[%s]+" % punctuation, ' ', line.lower())
        line = remove_invalid_tailo(line)
        line = re.sub(r'-', ' ', line)
        line = re.sub(r'\s+', ' ', line)
        text.append(ID+" "+line.strip())
    return text

### Replace punctuation with space and remove duplicate spaces
def clean_text_tailo_number_tone(intext):
    text = []
    for line in intext:
        ID, line = line.split(" ", 1)
        line = re.sub(r'[^a-z0-9\s-]', ' ', line.lower())
        line = re.sub(r'-', ' ', line)
        line = re.sub(r'\s+', ' ', line)
        text.append(ID+" "+line.strip())
    return text

### Replace punctuation with space and remove duplicate spaces
def clean_text_tailo_toneless(intext):
    text = []
    for line in intext:
        ID, line = line.split(" ", 1)
        line = re.sub(r'[0-9]', '', line.lower())
        line = re.sub(r'[^a-z\s-]', ' ', line.lower())
        line = re.sub(r'-', ' ', line.lower())
        line = re.sub(r'\s+', ' ', line)
        text.append(ID+" "+line.strip())
    return text

# Replace punctuation with space and remove duplicate spaces
def clean_text_en(intext):

    text = []
    for line in intext:
        ID, line = line.split(" ", 1)
        line = re.sub(r'[^a-z0-9\s-]', ' ', line.lower())
        line = re.sub(r'\s+', ' ', line)
        text.append(ID+" "+line.strip())
    return text

# remove all symbols from a text except for those used in Pe̍h-ōe-jī (POJ)
def clean_text_pei_oe_ji(intext):
    # Define the valid POJ character set including diacritics, space, and hyphen
    valid_poj_pattern = re.compile(r"[a-zA-Zô̍̄́̀̂ṳḿńǹêîâáàûúīíì\- ]+", re.UNICODE)
    
    # Find all valid POJ sequences and join them back into a string
    text = []
    for line in intext:
        ID, line = line.split(" ", 1)
        linw = ''.join(valid_poj_pattern.findall(line.lower()))
        text.append(ID+" "+line.strip())
    return text

def extract_id(input_string):
    # Split the string by underscores
    parts = input_string.split('_')
    
    # Extract the required parts
    part_1 = parts[3]  # This is 'TSM013'
    part_2 = parts[1] + '-' + parts[2]  # This is '0034_6.8'
    
    # Combine the parts to form the ID
    final_id = f"{part_1}-{part_2}"
    
    return final_id

# Function to create Kaldi-style files
def create_kaldi_files(tsv_file, subset):
    # Load the TSV file
    df = pd.read_csv(tsv_file, sep='\t')

    # Prepare output files
    wav_scp = []
    utt2spk = []
    text_files = {
        'hok_text_tailo': [],
        'hok_text_tailo_number_tone': [],
        'hok_text_hanlo_tai': [],
        'hok_text_pei_oe_ji': [],
        'en_text': []
    }

    # Process each row in the dataframe
    for index, row in df.iterrows():

        utt_id = extract_id(row['id'])
        hok_audio = row['hok_audio']
        hok_speaker = row['hok_speaker']
        hok_duration = row['hok_duration']

        if hok_duration <= 29.5:
            # Create wav.scp line
            wav_scp.append(f"{utt_id} downloads/tat_open_source_final/tat_open_source/{subset}/{hok_audio}")

            # Create utt2spk line
            utt2spk.append(f"{utt_id} {hok_speaker}")

            # Create text lines for each text column
            for key in text_files:
                text_files[key].append(f"{utt_id} {row[key]}")        
#       	print(utt_id, key, row[key])
        else:
            print("Ignore long utterance: {utt_id}, {hok_audio}, {hok_duration} =", utt_id, hok_audio, hok_duration)
    
    # Write files to output directory
    output_dir= "data/" + subset
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, 'wav.scp'), 'w') as f:
        f.write('\n'.join(wav_scp) + '\n')

    with open(os.path.join(output_dir, 'utt2spk'), 'w') as f:
        f.write('\n'.join(utt2spk) + '\n')

    for key, lines in text_files.items():
        if   key == "hok_text_tailo":
            lines = clean_text_tailo(lines)
        elif key == "hok_text_tailo_number_tone":
            lines = clean_text_tailo_number_tone(lines)
        elif key == "hok_text_hanlo_tai":
            lines = clean_text_hanlo_tai(lines)
        elif key == "hok_text_pei_oe_ji":
            lines = clean_text_pei_oe_ji(lines)
        elif key == "en_text":
            lines = clean_text_en(lines)
        else:
            print ("not support")
            exit(-1)
        with open(os.path.join(output_dir, f'{key}.txt'), 'w') as f:
            f.write('\n'.join(lines) + '\n')

    for key, lines in text_files.items():
        if key == "hok_text_tailo_number_tone":
            lines = clean_text_tailo_toneless(lines)
            key1 =  "hok_text_tailo_toneless"
            with open(os.path.join(output_dir, f'{key1}.txt'), 'w') as f:
                f.write('\n'.join(lines) + '\n')

# Example usage
tsv_file = 'downloads/tat_open_source_final/tat_open_source/dev/dev.tsv'  # Replace with the path to your TSV file
subset = 'dev'  # Directory to save the Kaldi-style files
create_kaldi_files(tsv_file, subset)

tsv_file = 'downloads/tat_open_source_final/tat_open_source/test/test.tsv'  # Replace with the path to your TSV file
subset = 'test'  # Directory to save the Kaldi-style files
create_kaldi_files(tsv_file, subset)
