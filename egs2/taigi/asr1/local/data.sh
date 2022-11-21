#!/bin/bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

log() {
    local fname=${BASH_SOURCE[1]##*/}
    echo -e "$(date '+%Y-%m-%dT%H:%M:%S') (${fname}:${BASH_LINENO[0]}:${FUNCNAME[1]}) $*"
}
SECONDS=0


stage=0
nj=32
stop_stage=100000
train_set=train_all
valid_set=dev_all

test_sets="tat-vol1-test tat-vol2-test tat-edu-test"

lid=false # whether to use language id as additional label
use_noise=false
global_path=

log "$0 $*"
. ./path.sh || exit 1
. ./cmd.sh || exit 1
. utils/parse_options.sh || exit 1

# if [ $# -ne 0 ]; then
#     log "Error: No positional arguments are required."
#     exit 2
# fi

if [ ${stage} -le 1 ]; then
  # combine the sub sets into the train_set
  echo "Stage 0: Combine Multiple Train Data Source"
  utils/combine_data.sh --extra-files utt2num_frames data/${train_set} \
      data/train-data/{tat-vol1-train,tat-vol2-train,tat-edu}


  # combine the sub sets into the dev_set
  echo "Stage 0: Combine Multiple Dev Data Source"
  utils/combine_data.sh --extra-files utt2num_frames data/${valid_set} \
      data/train-data/{tat-vol1-dev,tat-vol2-dev,tat-edu-dev}
      # data/train-data/{NER-Trs-Vol1-eval,librispeech-dev_clean,tat-vol1-dev}

  if $use_noise; then
    echo "Use FaNT to add noise"
    train_set=${train_set}_noise
    rirsdir=
    noise_opt=()
    dir_opt=()
    dest_opt=()

    # use FaNT to increase data diversity
    noise_opt+=("/nfs/TS-1635AX/Corpora/musan")
    noise_opt+=("/nfs/TS-1635AX/Corpora/NOISE_DATASETs/TRAIN")
    for n in ${noise_opt[@]}; do
      srcdir=data/train_all
      _n=$(echo $n | awk -F'/' '{print $NF}')
      local/multi_condition/perturb_data_dir_fant_convert.sh --nj $nj \
                                                            --noisedir $n \
                                                            $srcdir
      dest_opt+=(${srcdir}_fant_${_n})
    done
    utils/data/combine_data.sh data/train_all_fant ${dest_opt[@]}
    rm -r ${dest_opt[@]}

    dir_opt+=(data/train_all_fant)
    dir_opt+=(data/train_all)

    # add RIRs, simulated RIRs, isotropic noises and point-source noises
    if [[ -n "$rirsdir" ]]; then
      srcdir=data/train_all_fant
      samplerate=16000
      # Make a version with reverberated speech
      rvb_opts=()
      rvb_opts+=(--rir-set-parameters "0.5, ${rirsdir}/simulated_rirs/smallroom/rir_list")
      rvb_opts+=(--rir-set-parameters "0.5, ${rirsdir}/simulated_rirs/mediumroom/rir_list")
      # Make a reverberated version of the SWBD+SRE list. Note that we don't add any
      # additive noise here.
      python3 steps/data/reverberate_data_dir.py "${rvb_opts[@]}" \
                                                --prefix "reverb" \
                                                --speech-rvb-probability 1 \
                                                --pointsource-noise-addition-probability 0 \
                                                --isotropic-noise-addition-probability 0 \
                                                --num-replications 1 \
                                                --source-sampling-rate $samplerate \
                                                ${srcdir} ${srcdir}_reverb
      dir_opt+=(${srcdir}_reverb)
    fi
    utils/data/combine_data.sh data/${train_set} ${dir_opt[@]}
    utils/fix_data_dir.sh data/${train_set}
  fi
fi

if [ ${stage} -le 2 ] && [ ${stop_stage} -ge 2 ] && $lid; then
    log "stage 2: Create Non-linguistic Symbols for Language ID"
    cut -f 2- data/${train_set}/text | grep -o -P '\[.*?\]|\<.*?\>' | sort | uniq > ${nlsyms_txt}
    log "save non-linguistic symbols in ${nlsyms_txt}"
fi

#if [ ${stage} -le 3 ] && [ ${stop_stage} -ge 3 ]; then
#  # use external data
#  echo "$0: preparing extra corpus for subword LM training..."
#  mkdir -p data/local/other_text
#  local/lm/prepare_extra_text.sh --normjobs $nj \
#                              --global-path $global_path \
#                              data/local/lm data/local/lm/corpus || exit 1
#  if [ ! -e data/local/other_text/text ]; then
#    # provide utterance id to each texts
#    find data/local/lm/norm -mindepth 1 -maxdepth 3 -type f | xargs cat > data/local/other_text/text
#  fi
#fi

if [ ${stage} -le 4 ] && [ ${stop_stage} -ge 4 ]; then
  for test in ${test_sets}; do
    cp -r data/test-data/${test} data
    utils/fix_data_dir.sh data/${test}
  done
fi



log "Successfully finished. [elapsed=${SECONDS}s]"
