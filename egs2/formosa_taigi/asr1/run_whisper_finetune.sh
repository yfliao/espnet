#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

train_set=train
valid_set=dev
test_sets="dev test"

#asr_config=conf/tuning/train_asr_whisper_medium_finetune.yaml
asr_config=conf/tuning/train_sot_asr_whisper_small.yaml
#asr_config=conf/tuning/train_asr_whisper_medium_lora_finetune.yaml
#sr_config=cconf/tuning/train_asr_whisper_large_lora_finetune.yaml
inference_config=conf/tuning/decode_asr_whisper_noctc_beam10.yaml

lm_config=conf/train_lm_transformer.yaml
use_lm=false
use_wordlm=false

# speed perturbation related
# (train_set will be "${train_set}_sp" if speed_perturb_factors is specified)
speed_perturb_factors="0.9 1.0 1.1"

./asr.sh \
    --nj 32 \
    --ngpu 2 \
    --gpu_inference true \
    --inference_nj 1 \
    --lang en \
    --token_type whisper_multilingual \
    --feats_normalize "" \
    --audio_format "wav" \
    --feats_type raw \
    --use_lm ${use_lm}                                 \
    --use_word_lm ${use_wordlm}                        \
    --lm_config "${lm_config}"                         \
    --cleaner whisper_basic                            \
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
    --asr_args "--max_epoch 1"
