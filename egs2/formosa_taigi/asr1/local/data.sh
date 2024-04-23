#!/usr/bin/env bash

mkdir -p data/all
mkdir -p downloads
cd downloads

if [ ! -f SuiSiann-0.2.1.tar ]; then
	wget https://tongan-puntiunn.ithuan.tw/SuiSiann/SuiSiann-0.2.1.tar
fi

tar vxf SuiSiann-0.2.1.tar
cd ..

python local/SuiSiann.py
