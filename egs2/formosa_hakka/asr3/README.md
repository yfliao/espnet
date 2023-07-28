# 客語拼音輸出

修改egs2/aishell/asr1腳本，token_type改用bpe，加上wavlm_large前級。以下是主要更動：

## run.sh
```
...
./asr.sh \
    ...
    --ngpu 1 \
    --lang en \
    --audio_format "wav" \
    --token_type bpe \
    --bpe_train_text "data/${train_set}/text" \
    --nbpe 735 \
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

# Transcript

將FSR-2023-Hakka-Lavalier-Train語料庫下之train.csv檔案，處理成如下圖之文字擋。最終只保留音檔編號與客語拼音符號。

```
❯ head downloads/data_hakka/transcript/hakka_transcript.txt
F0010001A2007_1_07 ngin11 og2 ngin11 pa55 tien24 m11 pa55 ngin11 san55 ngin11 ki24 tien24 bud2 ki24
F0010001A2007_10_07 den31 ded2 ngied5 cud2 ngid2 log5 xi24
F0010001A2007_100_07 zun31 sui31 ngien11 ha24 e31 ca11 hed2 sang11 ha55 e31 cu31 fun55 song55 cam55 e31
F0010001A2007_101_07 vog5 teu11 dab5 vu24 in11 jiu31 ngiong11 ien11 xien55 e31 fad2 gau55 ngiau55 kiun11 e31
F0010001A2007_102_07 bai11 zog2 nen55 zu24 e31 fo31 teu11 nga11 gog5 e31 lung11 cong11 bi11 bi55 e31
F0010001A2007_103_07 pong55 giang55 to31 gung24 lo11 lib2 ma11 va31 tai55 pien31 con24 mun11 xiag2 go55 teu11
F0010001A2007_104_07 cag5 mun11 xim24 gon24 e31 li11 ba24 zon31 ngoi55 ga24 lo11 e31 miang55 ton11 e31
F0010001A2007_105_07 heu55 sang24 ngin11 zui55 giang24 lo31 ngin11 ga24 nung11 gong31 do31 siin11 jid2
F0010001A2007_106_07 lo31 tai24 tung11 teu11 miang11 qion11 qion11 bi31 m11 ded2 bi31 ge55 mi24 miang11 qiu55 han11 ka55 ded2
F0010001A2007_107_07 ba24 zong31 ma11 tong55 a55 go55 hi55 ia31 se55 teu11 ngi11 zung31 bau24 hi31 loi11
```

## Conformer+wavlm_large result  
config:path_to/config/train_asr_conformer7_wavlm_large.yaml  
CER
|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_asr_model_valid.acc.ave/test|2187|210486|98.9|0.9|0.2|0.1|1.2|42.1|
|decode_asr_asr_model_valid.acc.best/test|2187|210486|98.7|1.1|0.3|0.2|1.5|47.1|  

WER  
|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|  
|---|---|---|---|---|---|---|---|---|  
|decode_asr_asr_model_valid.acc.best/test|   2187    |   37457   |   96.2     |   3.7   |    0.1    |    0.1   |    3.9   |    42.1    |  
|decode_asr_asr_model_valid.acc.ave/test|2187  |  37457  |  95.3   |  4.5   |   0.2   |   0.0    | 4.7 |   47.1  |  
