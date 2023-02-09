from ..common import *
from .common import *
from .load_dataframe import load_dataframe

# A row is recognized as a header row
# if it contains at least `RECOGNIZE_THRESHOLD`
# words listed in `RECOGNIZABLE_COLUMNS`.
RECOGNIZE_THRESHOLD = 5
RECOGNIZABLE_COLUMNS = IGNORED_COLUMNS + list(COLUMN_MAP.keys())
RECOGNIZE_NROWS = 5
MAX_SKIPROWS = 3


def detect_skiprows(file: FileStorage) -> int:
    for n in range(MAX_SKIPROWS + 1):
        df = load_dataframe(
            file,
            nrows=RECOGNIZE_NROWS,
            skiprows=n,
        )
        recognized_count = 0
        for word in RECOGNIZABLE_COLUMNS:
            if word in df.columns:
                recognized_count += 1
        if recognized_count >= RECOGNIZE_THRESHOLD:
            return n
    return MAX_SKIPROWS
