#!/bin/bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

# E2E model related
train_set=train_all
valid_set=dev_all
test_sets="tat-vol1-test tat-vol2-test tat-edu-test"
use_noise=false
global_path=`pwd`
nj=150
stage=0
stop_stage=10000

. ./path.sh
. ./cmd.sh
. ./utils/parse_options.sh

asr_config=conf/tuning/train_asr_streaming_conformer.yaml
lm_config=conf/tuning/train_lm_transformer.yaml
inference_config=conf/decode_asr_streaming.yaml

if "${use_noise}"; then train_set=${train_set}_noise; fi

./asr.sh \
    --stage $stage \
    --stop_stage $stop_stage \
    --use_streaming true \
    --use_lm false \
    --nj $nj \
    --lang tw \
    --ngpu 10 \
    --num_nodes 1 \
    --nbpe 5000 \
    --token_type word \
    --feats_type raw \
    --audio_format wav \
    --max_wav_duration 30 \
    --speed_perturb_factors "0.9 1.0 1.1" \
    --asr_config "${asr_config}" \
    --lm_config "${lm_config}" \
    --inference_config "${inference_config}" \
    --local_data_opts "--global-path $global_path --nj $nj --stage 1" \
    --train_set "${train_set}" \
    --valid_set "${valid_set}" \
    --test_sets "${test_sets}" \
    --lm_train_text "data/${train_set}/text" \
    --bpe_train_text "data/${train_set}/text" "$@"
    
