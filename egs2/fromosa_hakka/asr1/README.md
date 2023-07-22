# RESULTS
## Environments
- date: Sat Jul 22 06:37:30 CST 2023
- python version: 3.9.17 (main, Jul  5 2023, 20:41:20)  [GCC 11.2.0]
- espnet version: espnet 202304
- pytorch version: pytorch 2.0.1+cu118
- Git hash: 09584933cf6ad91e59e99738edb27ad89d8d4481
  - Commit date: Tue Jul 18 07:56:57 2023 +0200

## exp/asr_train_asr_branchformer_raw_en_bpe735_sp
### WER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_branchformer_asr_model_valid.acc.ave/test|2187|37456|93.8|5.9|0.3|0.1|6.3|45.1|

### CER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_branchformer_asr_model_valid.acc.ave/test|2187|210487|98.1|1.4|0.6|0.3|2.3|45.1|

### TER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|decode_asr_branchformer_asr_model_valid.acc.ave/test|2187|77036|96.1|3.3|0.5|0.1|4.0|45.1|

## exp/asr_train_asr_branchformer_raw_en_bpe735_sp/decode_asr_branchformer_asr_model_valid.acc.ave
### WER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|org/dev|2126|36245|93.9|6.0|0.1|0.1|6.1|39.3|

### CER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|org/dev|2126|203417|98.3|1.2|0.5|0.3|2.0|39.3|

### TER

|dataset|Snt|Wrd|Corr|Sub|Del|Ins|Err|S.Err|
|---|---|---|---|---|---|---|---|---|
|org/dev|2126|74861|95.9|3.3|0.8|0.1|4.2|39.3|
