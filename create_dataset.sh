#!/bin/sh

set -xe

python3 dataset_maker.py
uwuify -t $(nproc) messages_to_be_uwuified.txt messages_uwuified.txt

rm -f messages.txt messages_to_be_uwuified.txt

rm -rf dataset
mkdir -p dataset/{normal,uwu}
#mv messages_good.txt dataset/normal/normal_text_1.txt
#mv messages_uwuified.txt dataset/uwu/uwu_text_1.txt

set +x
python3 split_file.py messages_good.txt dataset/normal $(nproc)
python3 split_file.py messages_uwuified.txt dataset/uwu $(nproc)

rm messages_good.txt messages_uwuified.txt
