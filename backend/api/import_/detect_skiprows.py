from ..common import *
from .common import *
from .load_dataframe import load_dataframe

# A row is recognized as a header row
# if it contains at least `RECOGNIZE_THRESHOLD`
# words matched by `COLUMN_PATTERNS`.
RECOGNIZE_THRESHOLD = 5
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
        for col in df.columns:
            if any(
                (pattern.match(col) != None)
                for pattern_col, pattern in COLUMN_PATTERNS
            ):
                recognized_count += 1
        if recognized_count >= RECOGNIZE_THRESHOLD:
            return n
    return MAX_SKIPROWS
