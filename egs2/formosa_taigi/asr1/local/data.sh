#!/usr/bin/env bash

. ./path.sh

mkdir -p data/all
mkdir -p downloads
cd downloads

if [ ! -f SuiSiann-0.2.1.tar ]; then
	wget https://tongan-puntiunn.ithuan.tw/SuiSiann/SuiSiann-0.2.1.tar
fi

tar vxf SuiSiann-0.2.1.tar
cd ..

python local/SuiSiann.py

utils/fix_data_dir.sh data/all

# Assuming all data is in a directory called 'data/all'
cd data/all

# Shuffle the speaker list to ensure randomness
awk '{print $1}' spk2utt | shuf > shuffled_speakers.list

# Count total speakers and calculate splits
total_speakers=$(cat shuffled_speakers.list | wc -l)
num_train=$(echo "$total_speakers * 0.8 / 1" | bc)
num_dev=$(echo "($total_speakers - $num_train) / 2 / 1" | bc)
num_test=$num_dev

# Create speaker subsets
head -n $num_train shuffled_speakers.list > train_speakers.list
tail -n +$((num_train + 1)) shuffled_speakers.list | head -n $num_dev > dev_speakers.list
tail -n $num_test shuffled_speakers.list > test_speakers.list

# Function to create data subsets
create_subset() {
    subset=$1
    speakers_list=$2
    mkdir -p data/$subset
    utils/subset_data_dir.sh --spk-list data/all/$speakers_list data/all data/$subset
    utils/fix_data_dir.sh data/$subset
}

# Create training, development, and testing subsets
cd ../../

create_subset "train" "train_speakers.list"
create_subset "dev" "dev_speakers.list"
create_subset "test" "test_speakers.list"
