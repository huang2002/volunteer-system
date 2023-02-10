#!/usr/bin/env bash
if [[ -e .venv ]]; then {
    echo --------------------------
    echo .venv/ already exists.
    echo Initialization is skipped.
    echo --------------------------
    read -n 1 -p 'Press any key to continue...'
    exit 0
} else {
    echo -----------------------
    echo Initialization started.
    echo -----------------------
} fi

python -m venv .venv \
    && ./.venv/bin/python -m ensurepip \

./.venv/bin/python -m pip install -r requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && echo Initialization finished successfully!

echo;
read -n 1 -p 'Press any key to continue...'
