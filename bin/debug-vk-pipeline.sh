#!/usr/bin/env bash

echo $PWD

export PYTHONPATH=$PWD

args=$(cat .auth/vk-args)
echo ${args}

file=$(python script/server/task/vk-import.py ${args})
echo ${file}

ga_args=$(cat .auth/ga-args)
echo $ga_args

python script/server/task/ga-export-single.py \
    ./.auth/AdsHubApp-e4cbe154490b.json ${ga_args} \
    ${file} ./imported/