#!/bin/bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

# E2E model related
train_set=train_all
valid_set=dev_all
test_sets="librispeech-test_clean librispeech-test_other \
        tat-vol1-test tat-vol2-test tat-tmp-edu \
        NER-Trs-Vol1-test NER-Trs-Vol2-test NER-Trs-Vol3-test NER-Trs-Vol4-test"
use_noise=false
global_path=`pwd`
lid=true # whether to use language id as additional label
nj=150
stage=0
stop_stage=10000

. ./path.sh
. ./cmd.sh
. ./utils/parse_options.sh

asr_config=conf/tuning/train_asr_conformer.yaml
lm_config=conf/tuning/train_lm_transformer.yaml
inference_config=conf/decode_asr.yaml
nlsyms_txt=data/local/nlsyms.txt

if "${use_noise}"; then train_set=${train_set}_noise; fi
#--use_streaming true \
./asr.sh \
    --stage $stage \
    --stop_stage $stop_stage \
    --use_lm false \
    --nj $nj \
    --lang cht_eng_tw \
    --ngpu 10 \
    --num_nodes 1 \
    --nbpe 20000 \
    --token_type bpe \
    --feats_type raw \
    --audio_format wav \
    --max_wav_duration 30 \
    --speed_perturb_factors "0.9 1.0 1.1" \
    --asr_config "${asr_config}" \
    --lm_config "${lm_config}" \
    --inference_config "${inference_config}" \
    --local_data_opts "--global-path $global_path --nj $nj --nlsyms_txt ${nlsyms_txt} --lid ${lid}" \
    --train_set "${train_set}" \
    --valid_set "${valid_set}" \
    --test_sets "${test_sets}" \
    --bpe_nlsyms "[CHT],[EN],[TW]" \
    --lm_train_text "data/${train_set}/text" \
    --bpe_train_text "data/${train_set}/text" "$@" \
    --local_score_opts "--score_lang_id ${lid}" "$@"
    
