from ..common import *
from .common import *

# TODO: handle missing years

WHITESPACE_PATTERN = re.compile(r'\s+')
DATE_IGNORE_PATTERN_CN = re.compile(r'（[^）]*）')
DATE_IGNORE_PATTERN_EN = re.compile(r'\([^)]*\)')
DATE_SEP_EN = '-'
EXCEL_DATE_ORIGIN = pd.to_datetime('1900/1/1') \
    - pd.DateOffset(days=2)  # manual fix

DATE_PATTERN_CN = re.compile(r'''(?x)  # verbose mode
    (\d{4})年
    (\d{1,2})月
    (\d{1,2})(?:日|号)
''')

DATE_RANGE_PATTERN_CN_DOUBLE_YEARS = re.compile(r'''(?x)  # verbose mode
    # from
    (\d{4})年
    (\d{1,2})月
    (\d{1,2})(?:日|号)
    # separate
    (?:|到|至|-|~)
    # to
    (\d{4})年
    (\d{1,2})月
    (\d{1,2})(?:日|号)
''')

DATE_RANGE_PATTERN_CN_SINGLE_YEAR = re.compile(r'''(?x)  # verbose mode
    # from
    (\d{4})年
    (\d{1,2})月
    (\d{1,2})(?:日|号)
    # separate
    (?:|到|至|-|~)
    # to
    (\d{1,2})月
    (\d{1,2})(?:日|号)
''')


def handle_activity_date(
    df_result: pd.DataFrame,
    series_raw: pd.Series,
) -> NoReturn:

    # init
    df_result['activity_begin'] = pd.NaT
    df_result['activity_end'] = pd.NaT

    # expand values
    n = len(series_raw)
    assert len(df_result) == n
    for i in range(n):

        # Acceptable: datetime/int/str
        raw_value = series_raw.iloc[i]

        if isinstance(raw_value, datetime.datetime):

            begin_date = pd.to_datetime(raw_value)
            end_date = begin_date

        elif isinstance(raw_value, int):

            # Excel stores dates as an integer
            # which means the offset from `EXCEL_DATE_ORIGIN`.
            delta_date = pd.DateOffset(days=raw_value)
            begin_date = EXCEL_DATE_ORIGIN + delta_date
            end_date = begin_date

        else:

            if not isinstance(raw_value, str):
                raw_value = str(raw_value)

            # filter
            raw_value = re.sub(DATE_IGNORE_PATTERN_CN, '', raw_value)
            raw_value = re.sub(DATE_IGNORE_PATTERN_EN, '', raw_value)
            raw_value = re.sub(WHITESPACE_PATTERN, '', raw_value)

            # Try different patterns and save results
            # in `matched`, `begin_date` and `end_date`.

            matched = DATE_PATTERN_CN.fullmatch(raw_value)
            if matched:
                year = int(matched.group(1))
                month = int(matched.group(2))
                day = int(matched.group(3))
                begin_date = pd.to_datetime(
                    datetime.date(year, month, day)
                )
                end_date = begin_date

            if not matched:
                matched = DATE_RANGE_PATTERN_CN_SINGLE_YEAR \
                    .fullmatch(raw_value)
                if matched:
                    year = int(matched.group(1))
                    begin_month = int(matched.group(2))
                    begin_day = int(matched.group(3))
                    end_month = int(matched.group(4))
                    end_day = int(matched.group(5))
                    begin_date = pd.to_datetime(
                        datetime.date(year, begin_month, begin_day)
                    )
                    end_date = pd.to_datetime(
                        datetime.date(year, end_month, end_day)
                    )

            if not matched:
                matched = DATE_RANGE_PATTERN_CN_DOUBLE_YEARS \
                    .fullmatch(raw_value)
                if matched:
                    begin_year = int(matched.group(1))
                    begin_month = int(matched.group(2))
                    begin_day = int(matched.group(3))
                    end_year = int(matched.group(4))
                    end_month = int(matched.group(5))
                    end_day = int(matched.group(6))
                    begin_date = pd.to_datetime(
                        datetime.date(begin_year, begin_month, begin_day)
                    )
                    end_date = pd.to_datetime(
                        datetime.date(end_year, end_month, end_day)
                    )

            if not matched:
                try:
                    if DATE_SEP_EN in raw_value:
                        sep_index = raw_value.index(DATE_SEP_EN)
                        begin_date = pd.to_datetime(raw_value[:sep_index])
                        end_date = pd.to_datetime(raw_value[(sep_index + 1):])
                    else:
                        begin_date = pd.to_datetime(raw_value)
                        end_date = begin_date
                except:
                    raise ImportTableError(
                        f'无法识别的日期：{raw_value}'
                    )

        index = df_result.index[i]
        df_result.loc[index, 'activity_begin'] = begin_date
        df_result.loc[index, 'activity_end'] = end_date
