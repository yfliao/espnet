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
