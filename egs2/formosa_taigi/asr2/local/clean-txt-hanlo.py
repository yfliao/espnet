import string
from zhon.hanzi import punctuation
import re
import os

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

# Define a function to clean the text
def clean_text_hanlo(text):
    text = re.sub(r"[%s]+" % punctuation, ' ', text.lower())
    text = remove_punctuation_except_hyphen(text)
    text = re.sub(r'\s+', ' ', text)
    text = remove_spaces_between_cjk_and_tailo(text)
    return text.strip()


def process_file(input_file, output_file):
    filename = os.path.splitext(input_file)[0]
    i = 0
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            cleaned_line = clean_text_hanlo(line)
            if cleaned_line:  # Only write non-empty lines
                i = i + 1
                outfile.write(filename + "-" + str(i+1000000) + " " + cleaned_line + '\n')

# Example usage
input_file = 'sentences-hanlo.txt'
output_file = 'sentences-hanlo-cleaned-index.txt'
process_file(input_file, output_file)

input_file = 'words-hanlo.txt'
output_file = 'words-hanlo-cleaned-index.txt'
process_file(input_file, output_file)
