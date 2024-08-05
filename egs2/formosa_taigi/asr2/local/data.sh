#!/usr/bin/env bash

. ./path.sh

mkdir -p data/all
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

if [ ! -f ESC-50-master.zip ]; then
        https://github.com/karoldvl/ESC-50/archive/master.zip
        unzip ESC-50-master.zip
fi

cd ..

mkdir -p data/train data/eval data/test

find downloads/TAT-MOE-Lavalier/Train -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $1"/"$3"/"$4"/"$5"/"$6".wav"}' > data/train/wav.scp
find downloads/TAT-MOE-Lavalier/Eval  -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $1"/"$3"/"$4"/"$5"/"$6".wav"}' > data/eval/wav.scp
find downloads/TAT-MOE-Lavalier/Test  -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $1"/"$3"/"$4"/"$5"/"$6".wav"}' > data/test/wav.scp

find downloads/TAT-MOE-Lavalier/Train -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $5}' > data/train/utt2spk
find downloads/TAT-MOE-Lavalier/Eval  -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $5}' > data/eval/utt2spk
find downloads/TAT-MOE-Lavalier/Test  -name '*.wav' | tr '/' ' ' | sed 's/.wav//' | awk '{print $5"_"$6, $5}' > data/test/utt2spk

python local/SuiSiann.py
cp data/all/texts data/all/text
utils/fix_data_dir.sh data/all

# Assuming all data is in a directory called 'data/all'
cd data/all

# Shuffle the utterance list to ensure randomness
awk '{print $1}' utt2spk | shuf > shuffled_utterances.list

# Count total utterances and calculate splits
total_utterances=$(cat shuffled_utterances.list | wc -l)
echo total_utterances=$total_utterances
num_train=$(echo "$total_utterances * 0.9 / 1" | bc)
num_dev=$(echo "($total_utterances - $num_train) / 2 / 1" | bc)
num_test=$num_dev
echo "num_train, num_dev, num_test=$num_train, $num_dev, $num_test"

# Create utterance subsets
head -n $num_train shuffled_utterances.list > train_utterances.list
tail -n +$((num_train + 1)) shuffled_utterances.list | head -n $num_dev > dev_utterances.list
tail -n $num_test shuffled_utterances.list > test_utterances.list

# Create training, development, and testing subsets
cd ../../

# Function to create data subsets
create_subset() {
    subset=$1
    utterances_list=$2
    mkdir -p data/$subset
    utils/subset_data_dir.sh --utt-list data/all/$utterances_list data/all data/$subset
    utils/fix_data_dir.sh data/$subset
}

create_subset "train" "train_utterances.list"
create_subset "dev" "dev_utterances.list"
create_subset "test" "test_utterances.list"
