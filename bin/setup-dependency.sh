#!/bin/bash

set -xeu

# Sets up test dependencies

cd "$(dirname "$0")/.."

if [ ! -d .ve ]; then
    virtualenv -p python3.7 .ve
fi

set +xeu
source .ve/bin/activate
set -xeu

pip3.7 install -r requirements.txt