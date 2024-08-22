#!/usr/bin/env bash

. ./path.sh

# Default language
lang="tailo-toneless"

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
    cp /nfs/RS2416RP/Corpora/TAT-MOE-Lavalier/TAT-MOE-Lavalier.zip .

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

if [ ! -f tat_open_source_final.zip ]; then
        wget https://sites.google.com/nycu.edu.tw/sarc/tat_s2st_benchmark/tat_open_source_final.zip #not work
        unzip tat_open_source_final.zip
fi


cd ..

find downloads/TAT-MOE-Lavalier/Train -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $1"/"$2"/"$3"/"$4"/"$5"/"$6".wav"}' > data/train/wav.scp
find downloads/TAT-MOE-Lavalier/Eval  -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $1"/"$2"/"$3"/"$4"/"$5"/"$6".wav"}' >> data/train/wav.scp
find downloads/TAT-MOE-Lavalier/Test  -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $1"/"$2"/"$3"/"$4"/"$5"/"$6".wav"}' >> data/train/wav.scp

find downloads/TAT-MOE-Lavalier/Train -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $5}' > data/train/utt2spk
find downloads/TAT-MOE-Lavalier/Eval  -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $5}' >> data/train/utt2spk
find downloads/TAT-MOE-Lavalier/Test  -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $5}' >> data/train/utt2spk

python local/TAT-MOE.py
python local/tat_open_source_final.py

cp  downloads/tat_open_source_final/tat_open_source/dev/utt2spk data/eval/utt2spk
sort -t$'\t' -k1,1 data/eval/utt2spk -o data/eval/utt2spk
cp  downloads/tat_open_source_final/tat_open_source/test/utt2spk data/test/utt2spk
sort -t$'\t' -k1,1 data/eval/utt2spk -o data/eval/utt2spk


cp  downloads/tat_open_source_final/tat_open_source/dev/wav.scp data/eval/wav.scp
cp  downloads/tat_open_source_final/tat_open_source/test/wav.scp data/test/wav.scp


# Your script logic here, using $LANGUAGE
if [[ "$lang" == "hanlo" ]]; then
    echo "Hanlo"
    cp downloads/TAT-MOE-Lavalier/Train/hanlo.txt data/train/text
    cat downloads/TAT-MOE-Lavalier/Eval/hanlo.txt >> data/train/text
    cat downloads/TAT-MOE-Lavalier/Test/hanlo.txt >> data/train/text

    cp  downloads/tat_open_source_final/tat_open_source/dev/hanlo.txt data/eval/text
    cp  downloads/tat_open_source_final/tat_open_source/test/hanlo.txt data/test/text
elif [[ "$lang" == "tailo" ]]; then
    echo "Hanlo"
    cp downloads/TAT-MOE-Lavalier/Train/tailo.txt data/train/text
    cat downloads/TAT-MOE-Lavalier/Eval/tailo.txt >> data/train/text
    cat downloads/TAT-MOE-Lavalier/Test/tailo.txt >> data/train/text

    cp  downloads/tat_open_source_final/tat_open_source/dev/tailo.txt data/eval/text
    cp  downloads/tat_open_source_final/tat_open_source/test/tailo.txt data/test/text
elif [[ "$lang" == "tailo-tone" ]]; then
    echo "Hanlo"
    cp downloads/TAT-MOE-Lavalier/Train/tailo-tone.txt data/train/text
    cat downloads/TAT-MOE-Lavalier/Eval/tailo-tone.txt >> data/train/text
    cat downloads/TAT-MOE-Lavalier/Test/tailo-tone.txt >> data/train/text

    cp  downloads/tat_open_source_final/tat_open_source/dev/tailo-tone.txt data/eval/text
    cp  downloads/tat_open_source_final/tat_open_source/test/tailo-tone.txt data/test/text
elif [[ "$lang" == "tailo-toneless" ]]; then
    echo "tailo-toneless"
    cp downloads/TAT-MOE-Lavalier/Train/tailo-toneless.txt data/train/text
    cat downloads/TAT-MOE-Lavalier/Eval/tailo-toneless.txt >> data/train/text
    cat downloads/TAT-MOE-Lavalier/Test/tailo-toneless.txt >> data/train/text

    cp  downloads/tat_open_source_final/tat_open_source/dev/tailo-toneless data/eval/text
    cp  downloads/tat_open_source_final/tat_open_source/test/tailo-toneless data/test/text
else
    echo "Unsupported language: $lang"
    exit 1
fi

utils/fix_data_dir.sh data/train

python local/tat_open_source_final.py

# Your script logic here, using $LANGUAGE
if [[ "$lang" == "hanlo" ]]; then
    echo "Hanlo"
    cat data/dev/hok_text_hanlo_tai.txt > data/dev/text
    cat data/test/hok_text_hanlo_tai.txt > data/test/text
elif [[ "$lang" == "tailo" ]]; then
    echo "Tailo"
    cat data/dev/hok_text_tailo.txt > data/dev/text
    cat data/test/hok_text_tailo.txt > data/test/text
elif [[ "$lang" == "tailo-tone" ]]; then
    echo "Tailo-Tone"
    cat data/dev/hok_text_tailo_number_tone.txt > data/dev/text
    cat data/test/hok_text_tailo_number_tone.txt > data/test/text
elif [[ "$lang" == "tailo-toneless" ]]; then
    echo "Tailo-toneless"
    cat data/dev/hok_text_tailo_toneless.txt > data/dev/text
    cat data/test/hok_text_tailo_toneless.txt > data/test/text
else
    echo "Unsupported language: $lang"
    exit 1
fi

utils/fix_data_dir.sh data/dev
utils/fix_data_dir.sh data/test

