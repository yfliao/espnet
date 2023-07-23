# 客語漢字輸出

修改egs2/aishell/asr1腳本，token_type沿用char，並控制RAM使用量<24GB，以下是主要更動：

## run.sh
```
...
./asr.sh \
    ...
    --ngpu 1 \
    --audio_format "wav" \
    ...
```

## conf/train_asr_branchformer.yaml
```
# minibatch related
...
batch_bins: 4300000
```

# Hakka data location & partition
```
downloads
└── data_hakka
    ├── transcript
    │   └── hakka_transcript.txt
    └── wav
        ├── dev
        │   ├── F002
        │   ├── F007
        │   ├── F127
        │   ├── F134
        │   ├── M002
        │   ├── M008
        │   ├── M127
        │   └── M129
        ├── test
        │   ├── F001
        │   ├── F006
        │   ├── F128
        │   ├── F132
        │   ├── M007
        │   ├── M009
        │   ├── M128
        │   └── M130
        └── train
            ├── F008
            ├── F013
            ├── F014
            ├── F015
            ├── F016
            ├── F018
            ├── F022
            ├── F023
            ├── F028
            ├── F031
            ├── F033
            ├── F034
            ├── F039
            ├── F040
            ├── F043
            ├── F044
            ├── F047
            ├── F049
            ├── F050
            ├── F053
            ├── F054
            ├── F056
            ├── F101
            ├── F104
            ├── F106
            ├── F108
            ├── F109
            ├── F110
            ├── F111
            ├── F116
            ├── F117
            ├── F122
            ├── F124
            ├── F126
            ├── M010
            ├── M014
            ├── M015
            ├── M017
            ├── M025
            ├── M037
            ├── M101
            ├── M102
            ├── M103
            ├── M104
            ├── M105
            ├── M106
            ├── M107
            ├── M108
            ├── M110
            ├── M111
            ├── M113
            ├── M114
            ├── M115
            ├── M116
            ├── M118
            ├── M120
            ├── M122
            ├── M124
            ├── M125
            └── M126
```

# Transcript
```
❯ head downloads/data_hakka/transcript/hakka_transcript.txt
F0010001A2007_1_07 人惡人怕天毋怕人善人欺天不欺
F0010001A2007_10_07 等得月出日落西
F0010001A2007_100_07 撙水年下仔查核成下仔處分上站仔
F0010001A2007_101_07 鑊頭搭烏蠅酒娘鉛線仔發酵尿裙仔
F0010001A2007_102_07 排桌乳珠仔伙頭牙确仔籠床嗶嗶仔
F0010001A2007_103_07 膨鏡討功勞笠嫲偎大片閂門惜過頭
F0010001A2007_104_07 柵門心肝仔籬笆轉外家籮仔命團仔
F0010001A2007_105_07 後生人最驚老人家噥講著成績
F0010001A2007_106_07 老弟同頭名全全比毋得比該尾名就還較得
F0010001A2007_107_07 巴掌嫲盪啊過去這事頭你總包起來
```

# RESULTS
## Environments
- date: Sat Jul 22 15:50:18 CST 2023
- python version: 3.9.17 (main, Jul  5 2023, 20:41:20)  [GCC 11.2.0]
- espnet version: espnet 202304
- pytorch version: pytorch 2.0.1+cu118
- Git hash: 09584933cf6ad91e59e99738edb27ad89d8d4481
  - Commit date: Tue Jul 18 07:56:57 2023 +0200

## exp/asr_train_asr_branchformer_raw_zh_char_sp
### WER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_branchformer_asr_model_valid.acc.ave/test|2187|2187|82.2|17.8|0.0|0.0|17.8|17.8|

### CER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_branchformer_asr_model_valid.acc.ave/test|2187|37473|94.1|5.0|0.9|0.2|6.1|17.8|

### TER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
## exp/asr_train_asr_branchformer_raw_zh_char_sp/decode_asr_branchformer_asr_model_valid.acc.ave
### WER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|org/dev|2126|2128|79.7|20.3|0.1|0.0|20.3|20.3|

### CER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|org/dev|2126|36270|93.2|5.9|0.8|0.3|7.0|20.3|

### TER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
2023-07-22T15:50:20 (asr.sh:1838:main) Successfully finished. [elapsed=27088s]
