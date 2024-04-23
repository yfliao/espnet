#!/usr/local/bin/python

import os
import csv
from pathlib import Path

dir = os.getcwd()

wav=[]
textc=[]
textp=[]
utt2spk=[]

with open('downloads/0.2.1/SuiSiann.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        id = Path(row['音檔']).stem
        wav.append([id, dir+"/downloads/0.2.1/"+row['音檔']])
        textc.append([id, row['漢字']])
        textp.append([id, row['羅馬字']])
        utt2spk.append([id, id])

with open('data/all/wav.scp', 'w') as file:
    for row in wav:
        file.write(' '.join(map(str, row)) + '\n')

with open('data/all/textc', 'w') as file:
    for row in textc:
        file.write(' '.join(map(str, row)) + '\n')

with open('data/all/textp', 'w') as file:
    for row in textp:
        file.write(' '.join(map(str, row)) + '\n')

with open('data/all/utt2spk', 'w') as file:
    for row in utt2spk:
        file.write(' '.join(map(str, row)) + '\n')
