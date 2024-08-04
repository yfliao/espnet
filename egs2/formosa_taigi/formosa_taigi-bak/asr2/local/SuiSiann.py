#!/usr/local/bin/python

import os
import csv
from pathlib import Path
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
import re

dir = os.getcwd()
wav=[]
textc=[]
textp=[]
textt=[]
texts=[]
utt2spk=[]

regex = re.compile('[^a-zA-Z0-9\s]')

with open('downloads/0.2.1/SuiSiann.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        
        id = Path(row['音檔']).stem
        wav.append([id, dir+"/downloads/0.2.1/"+row['音檔']])
        
        zh=row['漢字'].replace(' ','').replace('……','，').strip(' ')
        tailo=row['羅馬字'].replace('“','').replace('”','').replace('...',',').strip(' "').lower().strip(' ')
        tone=regex.sub(' ', 拆文分析器.建立句物件(tailo).轉音(臺灣閩南語羅馬字拼音).看語句().replace('-', ' '))
        tone=re.sub(' +',' ', tone).strip(' ')
        syllable=re.sub('[0-9]','', tone)

        textc.append([id, zh])
        textp.append([id, tailo])
        textt.append([id, tone])
        texts.append([id, syllable])
        
        utt2spk.append([id, 'Spk01'])


with open('data/all/wav.scp', 'w') as file:
    for row in wav:
        file.write(' '.join(map(str, row)) + '\n')

with open('data/all/textc', 'w') as file:
    for row in textc:
        file.write(' '.join(map(str, row)) + '\n')

with open('data/all/textp', 'w') as file:
    for row in textp:
        file.write(' '.join(map(str, row)) + '\n')

with open('data/all/textt', 'w') as file:
    for row in textt:
        file.write(' '.join(map(str, row)) + '\n')

with open('data/all/texts', 'w') as file:
    for row in texts:
        file.write(' '.join(map(str, row)) + '\n')

with open('data/all/utt2spk', 'w') as file:
    for row in utt2spk:
        file.write(' '.join(map(str, row)) + '\n')
