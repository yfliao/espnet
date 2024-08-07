#!/usr/bin/env bash

. ./path.sh

# Default language
lang="en"

# Parse options
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --lang)
            lang="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Print the selected language
echo "Selected language: $lang"

# processing TAT-MOE corpus

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

# Your script logic here, using $LANGUAGE
if [[ "$lang" == "en" ]]; then
    echo "Tailo-Toneless"
    cp data/train/tailo-toneless.txt data/train/text
    cp data/eval/tailo-toneless.txt data/eval/text
    cp data/test/tailo-toneless.txt data/test/text
elif [[ "$lang" == "zh" ]]; then
    echo "Hanlo"
    cp data/train/hanlo.txt data/train/text
    cp data/eval/hanlo.txt data/eval/text
    cp data/test/hanlo.txt data/test/text
else
    echo "Unsupported language: $LANGUAGE"
    exit 1
fi

utils/fix_data_dir.sh data/train
utils/fix_data_dir.sh data/eval
utils/fix_data_dir.sh data/test
