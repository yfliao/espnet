# ESPnet台灣台語
## Environments
- date: `Tue Aug 6 15:40:32 CDT 2024`
- python version: `3.9.18 (main, Sep 11 2023, 13:41:44)  [GCC 11.2.0]`
- espnet version: `espnet 202308`
- pytorch version: `pytorch 1.13.1`
## 安裝
請參考[ESPnet_install](https://espnet.github.io/espnet/installation.html)依照指示進行安裝，接著請安裝kenlm，這個在ESPnet安裝指示沒有提到，如果不安裝腳本執行會失敗
```bash
cd espnet/tools/
make kenlm.done
```

如果要使用Whisper ，請再使用腳本前先確保先執行以下步驟，並確保虛擬環境已經激活

請先找到tools資料夾裡面的installers
```bash
cd espnet/tools/installers/
conda activate espnet
bash install_whisper.sh
```

如果要使用LoRA，請再使用腳本前先確保 
```bash
conda activate espnet
pip install loralib
```
Lora參考網址 [link](https://github.com/microsoft/LoRA)

額外安裝項目，為了處理語料庫我們需要您在使用前安裝
```python
conda activate espnet
pip install tai5-uan5_gian5-gi2_kang1-ku7  # 安裝臺灣言語工具
pip install audiomentations
pip install nlpaug
```
台灣言語工具參考網址[link](https://i3thuan5.github.io/tai5-uan5_gian5-gi2_kang1-ku7/%E5%AE%89%E8%A3%9D.html)
## 語料
使用的是來自意傳公司的臺灣媠聲資料集 [SuíSiann Dataset](https://suisiann-dataset.ithuan.tw/)，內有台灣台語wav還有台羅和漢字及其他資訊，整個資料集共3467句，我們團隊有增加雜訊並擴充成兩倍
在我們的腳本執行時，會將資料集分成train、dev、test

|dataset|資料量|演講者數量|
|---|---|---|
|SuíSiann-train|6240|1|
|SuíSiann-dev|347|1|
|SuíSiann-test|347|1|

## 模型使用&腳本
- Transformer
  - [run.sh ](https://github.com/yfliao/espnet/blob/master/egs2/formosa_taigi/asr1/run.sh)
- Whisper(small、medium、large)
  - [run_whisper_finetune.sh](https://github.com/yfliao/espnet/blob/master/egs2/formosa_taigi/asr1/run_whisper_finetune.sh)
- Whisper_lora(small、medium、large)
  - [run_whisper_lora_finetune.sh](https://github.com/yfliao/espnet/blob/master/egs2/formosa_taigi/asr1/run_whisper_lora_finetune.sh)

使用的模型可以更改，只需要在腳本的`asr_config`和`inference_config`替換成想要的，腳本的其他設置可以根據實際用途進行更改。

## 使用
確保環境架設完成後，根據自己的需求執行`bash run.sh ` 、`bash run_whisper_finetune.sh ` 、`bash run_whisper_lora_finetune.sh ` ，執行腳本後會自動下載媠聲資料集和雜訊資料集，後面會進行雜訊跟隨機分配訓練集、驗證集、測試集，接著訓練跟進行測試。

## 實驗結果

# Transformer

## With Transformer LM
- Model link: (wait for upload)
- ASR config: [./conf/train_asr_branchformer.yaml](https://github.com/yfliao/espnet/blob/master/egs2/formosa_taigi/asr1/conf/train_asr_branchformer.yaml)
- LM config: [./conf/tuning/train_lm_transformer.yaml](https://github.com/yfliao/espnet/blob/master/egs2/formosa_taigi/asr1/conf/tuning/train_lm_transformer.yaml)

### WER(有加雜訊)

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_branchformer_asr_model_valid.acc.ave/test|347|5102|90.8|9.0|0.2|0.4|9.6|52.4|
|org/dev|347|5150|89.0|10.1|0.9|0.6|11.6|52.7|

# Whisper Small Full Finetune
## Results

- ASR config: [conf/tuning/train_asr_whisper_small_finetune.yaml](https://github.com/yfliao/espnet/blob/master/egs2/formosa_taigi/asr1/conf/tuning/train_asr_whisper_small_finetune.yaml)
- Decode config: [conf/tuning/decode_asr_whisper_noctc_beam10.yaml](https://github.com/yfliao/espnet/blob/master/egs2/formosa_taigi/asr1/conf/tuning/decode_asr_whisper_noctc_beam10.yaml)

### WER(有加雜訊)

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_whisper_noctc_beam10_asr_model_valid.acc.ave/test|347|5610|93.5|6.1|0.4|0.2|6.7|36.6|
|org/dev|347|5586|94.9|4.8|0.3|0.2|5.2|34.3|

# Whisper Small LoRA finetune
## Results

- ASR config: [conf/tuning/train_asr_whisper_small_lora_finetune.yaml](conf/tuning/train_asr_whisper_small_lora_finetune.yaml)
- Decode config: [conf/tuning/decode_asr_whisper_noctc_beam10.yaml](conf/tuning/decode_asr_whisper_noctc_beam10.yaml)
- Pretrained Model:
  - #Trainable Params: 4.72 M
  - Link: TBD

### WER(有加雜訊)

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_whisper_noctc_beam10_asr_model_valid.acc.ave/test|347|5102|89.8|6.5|3.6|0.2|10.4|10.4|
|org/dev|347|5150|92.5|5.0|2.6|0.1|7.7|8.9|



# Whisper Medium Full Finetune
## Results

- ASR config: [conf/tuning/train_asr_whisper_medium_finetune.yaml](conf/tuning/train_asr_whisper_medium_finetune.yaml)
- Decode config: [conf/tuning/decode_asr_whisper_noctc_beam10.yaml](conf/tuning/decode_asr_whisper_noctc_beam10.yaml)
- Pretrained Model:
  - #Params: 762.32 M

### WER(無加雜訊)

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_whisper_noctc_beam10_asr_model_valid.acc.ave/test|173|3003|99.5|0.4|0.1|0.0|0.5|7.5|
|org/dev|173|2703|97.3|0.6|2.0|0.0|2.7|8.7|

# Whisper Medium LoRA finetune
## Results

- ASR config: [conf/tuning/train_asr_whisper_medium_lora_finetune.yaml](conf/tuning/train_asr_whisper_medium_lora_finetune.yaml)
- Decode config: [conf/tuning/decode_asr_whisper_noctc_beam10.yaml](conf/tuning/decode_asr_whisper_noctc_beam10.yaml)
- Pretrained Model:
  - #Trainable Params: 4.72 M
  - Link: TBD

### WER(有加雜訊)

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_whisper_noctc_beam10_asr_model_valid.acc.ave/test|347|5099|99.7|0.2|0.1|0.0|0.3|1.4|
|org/dev|347|5794|96.4|1.2|2.3|0.1|3.7|2.0|


# Whisper Large Full Finetune
## Results

- ASR config: [conf/tuning/train_asr_whisper_large_finetune.yaml](conf/tuning/train_asr_whisper_large_finetune.yaml)
- Decode config: [conf/tuning/decode_asr_whisper_noctc_beam10.yaml](conf/tuning/decode_asr_whisper_noctc_beam10.yaml)

### WER(無加雜訊)

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_whisper_noctc_beam10_asr_model_valid.acc.ave/test|173|3003|93.8|4.8|1.4|0.4|6.6|45.1|
|org/dev|173|2703|92.9|4.4|2.7|0.8|7.9|46.8|

# Whisper Large LoRA finetune
## Results

- ASR config: [conf/tuning/train_asr_whisper_large_lora_finetune.yaml](conf/tuning/train_asr_whisper_large_lora_finetune.yaml)
- Decode config: [conf/tuning/decode_asr_whisper_noctc_beam10.yaml](conf/tuning/decode_asr_whisper_noctc_beam10.yaml)
- Pretrained Model:
  - #Trainable Params: 7.86 M
  - Link: TBD

### WER(還沒)

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_whisper_noctc_beam10_asr_model_valid.acc.ave/dev|14326|205341|97.6|2.3|0.1|0.1|2.5|22.4|
|decode_asr_whisper_noctc_beam10_asr_model_valid.acc.ave/test|7176|104765|97.3|2.6|0.1|0.1|2.7|23.9|


