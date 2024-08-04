#!/usr/bin/env bash

. ./path.sh

mkdir -p data/all
mkdir -p downloads
cd downloads

if [ ! -f SuiSiann-0.2.1.tar ]; then
	wget https://tongan-puntiunn.ithuan.tw/SuiSiann/SuiSiann-0.2.1.tar
	tar vxf SuiSiann-0.2.1.tar
fi

if [ ! -f musan.tar.gz ]; then
	wget https://www.openslr.org/resources/17/musan.tar.gz
	tar vxfz musan.tar.gz
fi

if [ ! -f rirs_noises.zip ]; then
	wget https://www.openslr.org/resources/28/rirs_noises.zip
	unzip rirs_noises.zip
fi

if [ ! -f rirs_noises.zip ]; then
	https://github.com/karoldvl/ESC-50/archive/master.zip
	unzip master.zip
fi

cd ..

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
