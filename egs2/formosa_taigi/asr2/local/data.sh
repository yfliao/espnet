#!/usr/bin/env bash

. ./path.sh

mkdir -p data/train data/eval data/test
mkdir -p downloads
cd downloads

if [ ! -f TAT-MOE-Lavalier.zip ]; then
	wget https://tggl.naer.edu.tw/corpus_files/TAT-MOE-Lavalier.zip
	unzip TAT-MOE-Lavalier.zip
fi

if [ ! -f musan.tar.gz ]; then
	wget https://www.openslr.org/resources/17/musan.tar.gz
	tar vxfz musan.tar.gz
fi

if [ ! -f rirs_noises.zip ]; then
	wget https://www.openslr.org/resources/28/rirs_noises.zip
	unzip rirs_noises.zip
fi

if [ ! -f master.zip ]; then
        wget https://github.com/karoldvl/ESC-50/archive/master.zip
        unzip master.zip
fi

cd ..

find downloads/TAT-MOE-Lavalier/Train -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $1"/"$2"/"$3"/"$4"/"$5"/"$6".wav"}' > data/train/wav.scp
find downloads/TAT-MOE-Lavalier/Eval  -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $1"/"$2"/"$3"/"$4"/"$5"/"$6".wav"}' > data/eval/wav.scp
find downloads/TAT-MOE-Lavalier/Test  -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $1"/"$2"/"$3"/"$4"/"$5"/"$6".wav"}' > data/test/wav.scp

find downloads/TAT-MOE-Lavalier/Train -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $5}' > data/train/utt2spk
find downloads/TAT-MOE-Lavalier/Eval  -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $5}' > data/eval/utt2spk
find downloads/TAT-MOE-Lavalier/Test  -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $5}' > data/test/utt2spk

python local/TAT-MOE.py

cp data/train/tailo-toneless.txt data/train/text
cp data/eval/tailo-toneless.txt data/eval/text
cp data/test/tailo-toneless.txt data/test/text

utils/fix_data_dir.sh data/train
utils/fix_data_dir.sh data/eval
utils/fix_data_dir.sh data/test
