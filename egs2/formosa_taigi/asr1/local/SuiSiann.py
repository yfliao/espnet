#!/usr/local/bin/python

import os
import csv
from pathlib import Path
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音
import re

import glob
from scipy.io import wavfile
from audiomentations import Compose, SomeOf, AddGaussianNoise, AddGaussianSNR, TimeStretch, PitchShift, Shift, AddBackgroundNoise, AddShortNoises, PolarityInversion, ApplyImpulseResponse
from audiomentations.core.audio_loading_utils import load_sound_file
import nlpaug.augmenter.audio as naa
import nlpaug.flow as naf

sr = 22050

augment1 = naf.Sometimes([
    naa.VtlpAug(sampling_rate=sr, zone=(0.0, 1.0), coverage=1.0, factor=(0.9, 1.1)),
    ], aug_p=0.4)

augment2 = Compose([
    AddGaussianSNR(min_snr_in_db=10, max_snr_in_db=30, p=0.2),
    TimeStretch(min_rate=0.8, max_rate=1.2, leave_length_unchanged=False, p=0.4),
    PitchShift(min_semitones=-4, max_semitones=4, p=0.4),
    AddBackgroundNoise(
        sounds_path="downloads/musan/noise/free-sound",
        min_snr_in_db=10,
        max_snr_in_db=30.0,
        p=0.4),
    AddShortNoises(
    sounds_path="downloads//musan/noise/sound-bible",
    min_snr_in_db=10,
    max_snr_in_db=30.0,
    noise_rms="relative_to_whole_input",
    min_time_between_sounds=2.0,
    max_time_between_sounds=8.0,
    p=0.3),
    ApplyImpulseResponse(
            ir_path="downloads/RIRS_NOISES/simulated_rirs", p=0.4
        )
])

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
        ImTong=row['音檔'].split("/")[0]
        wav.append(["A"+id, dir+"/downloads/0.2.1/"+row['音檔'].replace('ImTong/','ImTong/A')])

        zh=row['漢字'].replace(' ','').replace('……','，').strip(' ')
        tailo=row['羅馬字'].replace('“','').replace('”','').replace('...',',').strip(' "').lower().strip(' ')
        tone=regex.sub(' ', 拆文分析器.建立句物件(tailo).轉音(臺灣閩南語羅馬字拼音).看語句().replace('-', ' '))
        tone=re.sub(' +',' ', tone).strip(' ')
        syllable=re.sub('[0-9]','', tone)

        textc.append([id, zh])
        textp.append([id, tailo])
        textt.append([id, tone])
        texts.append([id, syllable])
        
        textc.append(['A'+id, zh])
        textp.append(['A'+id, tailo])
        textt.append(['A'+id, tone])
        texts.append(['A'+id, syllable])
        utt2spk.append([id, 'Spk01'])
        utt2spk.append(['A'+id, 'Spk01'])

for data in wav:
    if data[0][0]=='A':
        file=data[0][1:]+".wav"
        InPath = "/".join(data[1].split("/")[:-1]) + "/"
        samples, sample_rate = load_sound_file(
            os.path.join(InPath, file), sample_rate=None
        )
        augmented_samples1 = augment1.augment(samples)
        augmented_samples2 = augment2(samples=augmented_samples1[0], sample_rate=sample_rate)
        file="A"+file
        wavfile.write(
            os.path.join(InPath, file), rate=sample_rate, data=augmented_samples2
        )
    elif data[0][0]=='S':
        continue
print("ok")
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
