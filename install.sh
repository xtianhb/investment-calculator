#!/bin/bash
set -e

sudo apt update
sudo apt install -y python3 python3-venv
sudo apt install -y python3-pip

ENV_NAME="env-inv"

if [[ ! -d $ENV_NAME ]]; then
    python3 -m venv $ENV_NAME
fi

source $ENV_NAME/bin/activate

pip3 install -r requirements.txt
