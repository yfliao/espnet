#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail


#Choose 台文漢字 or 台羅 for training (zh en )
traing_data="ch"
if [ "$traing_data" = "ch" ]; then
  nbpe=2447
  lang="zh"
  local_data_opts="textc"
fi
if [ "$traing_data" = "en" ]; then
  nbpe=30
  lang="en"
  local_data_opts="texts"
fi

all_set=all
train_set=train
valid_set=dev
test_sets="dev test"

#asr_config=conf/train_asr_transformer.yaml
asr_config=conf/train_asr_branchformer.yaml
inference_config=conf/decode_asr_branchformer.yaml

lm_config=conf/train_lm_transformer.yaml
use_lm=false
use_wordlm=false

# speed perturbation related
# (train_set will be "${train_set}_sp" if speed_perturb_factors is specified)
speed_perturb_factors="0.9 1.0 1.1"

./asr.sh \
    --nj 32 \
    --inference_nj 32 \
    --ngpu 8 \
    --lang ${lang} \
    --audio_format wav \
    --feats_type raw \
    --token_type bpe \
    --nbpe ${nbpe} \
    --use_lm ${use_lm}                                 \
    --use_word_lm ${use_wordlm}                        \
    --lm_config "${lm_config}"                         \
    --asr_config "${asr_config}"                       \
    --inference_config "${inference_config}"           \
    --train_set "${train_set}"                         \
    --valid_set "${valid_set}"                         \
    --test_sets "${test_sets}"                         \
    --speed_perturb_factors "${speed_perturb_factors}" \
    --asr_speech_fold_length 512 \
    --asr_text_fold_length 150 \
    --lm_fold_length 150 \
    --lm_train_text "data/${train_set}/text" "$@" \
    --bpe_train_text "data/${train_set}/text" "$@" \
    --feats_normalize uttmvn \
    --asr_args "--max_epoch 1" \
    --local_data_opts ${local_data_opts}
