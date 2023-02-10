@echo off

if exist .venv (
    echo --------------------------
    echo .venv/ already exists.
    echo Initialization is skipped.
    echo --------------------------
    pause
    exit 0
) else (
    echo -----------------------
    echo Initialization started.
    echo -----------------------
)

python -m venv .venv ^
    && .\.venv\Scripts\python -m ensurepip

.\.venv\Scripts\python -m pip install -r requirements.txt ^
    -i https://pypi.tuna.tsinghua.edu.cn/simple ^
    && echo Initialization finished successfully!

echo.
pause
