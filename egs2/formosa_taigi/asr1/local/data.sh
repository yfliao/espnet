#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

log() {
    local fname=${BASH_SOURCE[1]##*/}
    echo -e "$(date '+%Y-%m-%dT%H:%M:%S') (${fname}:${BASH_LINENO[0]}:${FUNCNAME[1]}) $*"
}
help_message=$(cat << EOF
Usage: $0

Options:
    --remove_archive (bool): true or false
      With remove_archive=True, the archives will be removed after being successfully downloaded and un-tarred.
EOF
)
SECONDS=0

# Data preparation related
data_url=tongan-puntiunn.ithuan.tw/SuiSiann
remove_archive=false
download_opt=

log "$0 $*"


. ./utils/parse_options.sh

. ./db.sh
. ./path.sh
. ./cmd.sh


if [ $# -gt 1 ]; then
  log "${help_message}"
  exit 2
fi

if "$remove_archive"; then
  download_opt="--remove-archive"
fi

if [ -z "${FORMOSA_TAIGI}" ]; then
  log "Error: \$FORMOSA_TAIGI is not set in db.sh."
  exit 2
fi


log "Download data to ${FORMOSA_TAIGI}"
if [ ! -d "${FORMOSA_TAIGI}" ]; then
    mkdir -p "${FORMOSA_TAIGI}"
fi
# To absolute path
FORMOSA_TAIGI=$(cd ${FORMOSA_TAIGI}; pwd)

echo local/download_and_untar.sh ${download_opt} "${FORMOSA_TAIGI}" "${data_url}" SuiSiann-0.2.1
local/download_and_untar.sh ${download_opt} "${FORMOSA_TAIGI}" "${data_url}" SuiSiann-0.2.1
#echo local/download_and_untar.sh ${download_opt} "${FORMOSA_TAIGI}" "${data_url}" resource_suisiann
#local/download_and_untar.sh ${download_opt} "${FORMOSA_TAIGI}" "${data_url}" resource_suisiann

suisiann_audio_dir=${FORMOSA_TAIGI}/0.2.1/ImTong
suisiann_text=${FORMOSA_TAIGI}/0.2.1/SuiSiann.csv

log "Data Preparation"
train_dir=data/local/train
dev_dir=data/local/dev
test_dir=data/local/test
tmp_dir=data/local/tmp

mkdir -p $train_dir
mkdir -p $dev_dir
mkdir -p $test_dir
mkdir -p $tmp_dir

# find wav audio file for train, dev and test resp.
find $suisiann_audio_dir -iname "*.wav" > $tmp_dir/wav.flist
n=$(wc -l < $tmp_dir/wav.flist)
[ $n -ne 141925 ] && \
  log Warning: expected 141925 data data files, found $n

grep -i "wav/train" $tmp_dir/wav.flist > $train_dir/wav.flist || exit 1;
grep -i "wav/dev" $tmp_dir/wav.flist > $dev_dir/wav.flist || exit 1;
grep -i "wav/test" $tmp_dir/wav.flist > $test_dir/wav.flist || exit 1;

rm -r $tmp_dir

# Transcriptions preparation
for dir in $train_dir $dev_dir $test_dir; do
  log Preparing $dir transcriptions
  sed -e 's/\.wav//' $dir/wav.flist | awk -F '/' '{print $NF}' > $dir/utt.list
  sed -e 's/\.wav//' $dir/wav.flist | awk -F '/' '{i=NF-1;printf("%s %s\n",$NF,$i)}' > $dir/utt2spk_all
  paste -d' ' $dir/utt.list $dir/wav.flist > $dir/wav.scp_all
  utils/filter_scp.pl -f 1 $dir/utt.list $suisiann_text > $dir/transcripts.txt
  awk '{print $1}' $dir/transcripts.txt > $dir/utt.list
  utils/filter_scp.pl -f 1 $dir/utt.list $dir/utt2spk_all | sort -u > $dir/utt2spk
  utils/filter_scp.pl -f 1 $dir/utt.list $dir/wav.scp_all | sort -u > $dir/wav.scp
  sort -u $dir/transcripts.txt > $dir/text
  utils/utt2spk_to_spk2utt.pl $dir/utt2spk > $dir/spk2utt
done

mkdir -p data/train data/dev data/test

for f in spk2utt utt2spk wav.scp text; do
  cp $train_dir/$f data/train/$f || exit 1;
  cp $dev_dir/$f data/dev/$f || exit 1;
  cp $test_dir/$f data/test/$f || exit 1;
done

# remove space in text
for x in train dev test; do
  cp data/${x}/text data/${x}/text.org
  paste -d " " <(cut -f 1 -d" " data/${x}/text.org) <(cut -f 2- -d" " data/${x}/text.org | tr -d " ") \
      > data/${x}/text
  rm data/${x}/text.org
done

log "Successfully finished. [elapsed=${SECONDS}s]"
