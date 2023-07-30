# 客語漢字輸出

修改egs2/aishell/asr1腳本，token_type沿用char，加上wavlm_large前級。以下是主要更動：

## run.sh
```
...
./asr.sh \
    ...
    --ngpu 1 \
    --audio_format "wav" \
    ...
    --feats_normalize utterance_mvn
```

## conf/train_asr_conformer+wavlm.yaml
```
frontend: s3prl
frontend_conf:
    frontend_conf:
        upstream: wavlm_large  # Note: If the upstream is changed, please change the input_size in the preencoder.
    download_dir: ./hub
    multilayer_feature: True

preencoder: linear
preencoder_conf:
    input_size: 1024  # Note: If the upstream is changed, please change this value accordingly.
    output_size: 80

# minibatch related
...
batch_bins: 3000000
```

# Hakka data location & partition

整個FSR-2023-Hakka-Lavalier-Train語料庫，以人跟性別為單位分割，隨機挑選4男4女為dev set，4男4女為test set，剩下的全部做為訓練用train set。資料處理完後以下列格式，存放在 downloads目錄下。

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

將FSR-2023-Hakka-Lavalier-Train語料庫下之train.csv檔案，處理成如下圖之文字擋。最終只保留音檔編號與客語漢字。

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
- date: `Sun Jul 30 04:54:52 CST 2023`
- python version: `3.10.12 (main, Jul  5 2023, 18:54:27) [GCC 11.2.0]`
- espnet version: `espnet 202304`
- pytorch version: `pytorch 2.0.1+cu118`
- Git hash: `d02e2759a310d88c83c78d1c070dc689dbf0d7d1`
  - Commit date: `Sat Jul 29 09:54:26 2023 +0800`

## exp/asr_train_asr_conformer+wavlm_raw_zh_char_sp
### WER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_lm_lm_train_lm_transformer2_zh_char_valid.loss.ave_asr_model_valid.acc.ave/test|2187|2187|50.0|50.0|0.0|0.0|50.0|50.0|

### CER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_lm_lm_train_lm_transformer2_zh_char_valid.loss.ave_asr_model_valid.acc.ave/test|2187|37473|93.3|3.0|3.7|0.0|6.7|50.0|

### TER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
## exp/asr_train_asr_conformer+wavlm_raw_zh_char_sp/decode_asr_lm_lm_train_lm_transformer2_zh_char_valid.loss.ave_asr_model_valid.acc.ave
### WER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|org/dev|2126|2128|53.7|46.2|0.1|0.0|46.3|46.2|

### CER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|org/dev|2126|36270|93.6|3.0|3.4|0.0|6.4|46.2|

### TER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
2023-07-30T04:54:55 (asr.sh:1838:main) Successfully finished. [elapsed=68493s]

# RESULTS
## Conformer+wavlm_large result  

訓練時間:3090*1 & 50小時  
config:path_to/config/train_asr_conformer7_wavlm_large.yaml  
CER  
|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|  
|---|---|---|---|---|---|---|---|---|  
|decode_asr_asr_model_valid.acc.best/test|2187|37473|96.8|2.2|1.0|0.1|3.3|17.4|  
