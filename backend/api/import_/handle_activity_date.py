from ..common import *
from .common import *

FILENAME_DATE_PATTERN = re.compile(r'(?<=\D)\d{4}(?=\D)')
EXCEL_DATE_ORIGIN = pd.to_datetime('1900/1/1') \
    - pd.DateOffset(days=2)  # manual fix

DATE_SEP_EN = '-'
DATE_SEP_COMPACT = r'-—－、，, '  # '-' must be the first
ADDITION_PATTERN = re.compile(r'[\(（][^)]*[\)）]')
MULTIPLE_DATE_PATTERN = re.compile(r'''(?x)  # verbose mode
    (\d{1,2}月\d{1,2}日)
    (?:-?\d{1,2}月\d{1,2}日)+
    -?(\d{1,2}月\d{1,2}日)
''')
MULTIPLE_RANGE_PATTERN = re.compile(f'''(?x)  # verbose mode
    [{DATE_SEP_COMPACT}]
    (?:[^{DATE_SEP_COMPACT}]+[{DATE_SEP_COMPACT}])*
''')
REPLACEMENT_PATTERNS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r'^\s+'), ''),
    (re.compile(r'\s+$'), ''),
    (ADDITION_PATTERN, ''),
    (MULTIPLE_DATE_PATTERN, r'\1-\2'),
    (MULTIPLE_RANGE_PATTERN, DATE_SEP_EN),
]

MONTH_PATTERN = re.compile(r'''(?x)  # verbose mode
    (?:(\d{4})(?:年|/|／|\.))?
    (\d{1,2})(?:月|/|／|\.|年|-)  # HACK
''')

DATE_PATTERN = re.compile(r'''(?x)  # verbose mode
    # date
    (?:(\d{4})(?:年|月|/|／|\.))?  # HACK
    (\d{1,2})(?:月|/|／|\.|年|-)  # HACK
    (\d{1,2})(?:日|号)?
    # optional time
    (?:\d{1,2}(?::|：|\.)\d{1,2})?
    (?:(?:—|——|-|－|~)\d{1,2}(?::|：|\.)\d{1,2})?
''')

DATE_RANGE_PATTERN = re.compile(r'''(?x)  # verbose mode
    # from
    (?:(\d{4})(?:年|月|/|／|\.))?  # HACK
    (\d{1,2})(?:月|/|／|\.|年)  # HACK
    (\d{1,2})(?:日|号)?
    # separate
    (?:—+|-+|－|~|:|：|到|至|及)  # HACK
    # to
    (?:(\d{4})(?:年|月|/|／|\.))?  # HACK
    (?:(\d{1,2})(?:月|/|／|\.|年))?  # HACK
    (\d{1,2})(?:日|号)?
    # optional time
    (?:\d{1,2}(?::|：|\.)\d{1,2}(?:—|——|-|－|~))?
    (?:\d{1,2}(?::|：|\.)\d{1,2})?
''')

DATE_OFFSET_TO_MONTH_END = pd.DateOffset(months=1, days=-1)
MONTH_RANGE_PATTERN = re.compile(r'''(?x)  # verbose mode
    # from
    (?:(\d{4})(?:年|/|／|\.))?
    (\d{1,2})(?:月|/|／|\.|年)?  # HACK
    # separate
    (?:—+|-+|－|~|:|：|到|至|及)  # HACK
    # to
    (?:(\d{4})(?:年|/|／|\.))?
    (?:(\d{1,2})(?:月|/|／|\.|年))?  # HACK
''')


def handle_activity_date(
    df_result: pd.DataFrame,
    series_raw: pd.Series,
    **params,
) -> NoReturn:

    # init
    df_result['activity_begin'] = pd.NaT
    df_result['activity_end'] = pd.NaT

    # guess default year from filename
    filename_year: Optional[int] = None
    matched = FILENAME_DATE_PATTERN.search(params['filename'])
    if matched:
        filename_year = int(matched.group(0))

    def parse_date_component(
        raw_component: str,
        *,
        default_value=filename_year,
        raw_value: Any,
    ) -> int:
        if raw_component:
            return int(raw_component)
        elif default_value:
            return default_value
        else:
            raise ImportTableError(
                f'无法确定年份的日期：{raw_value}'
            )

    # expand values
    n = len(series_raw)
    assert len(df_result) == n
    for i in range(n):

        # Acceptable: datetime/int/str
        raw_value = series_raw.iloc[i]

        if not raw_value:

            begin_date = pd.NaT
            end_date = pd.NaT

        elif isinstance(raw_value, datetime.datetime):

            begin_date = pd.to_datetime(raw_value)
            end_date = begin_date

        # Pandas stores integers as int64 numbers by default.
        elif isinstance(raw_value, (np.int64, int)):

            # Excel stores dates as an integer
            # which means the offset from `EXCEL_DATE_ORIGIN`.
            delta_date = pd.DateOffset(days=int(raw_value))
            begin_date = EXCEL_DATE_ORIGIN + delta_date
            end_date = begin_date

        else:

            raw_string = raw_value if isinstance(raw_value, str) \
                else str(raw_value)

            # filter
            for pattern, replacement in REPLACEMENT_PATTERNS:
                raw_string = pattern.sub(replacement, raw_string)

            # Try different patterns and save results
            # in `matched`, `begin_date` and `end_date`.
            try:

                matched = DATE_PATTERN.fullmatch(raw_string)
                if matched:
                    year = parse_date_component(
                        matched.group(1),
                        raw_value=raw_string,
                    )
                    month = int(matched.group(2))
                    day = int(matched.group(3))
                    begin_date = pd.to_datetime(
                        datetime.date(year, month, day)
                    )
                    end_date = begin_date

                if not matched:
                    matched = MONTH_PATTERN.fullmatch(raw_string)
                    if matched:
                        year = parse_date_component(
                            matched.group(1),
                            raw_value=raw_string,
                        )
                        month = int(matched.group(2))
                        begin_date = pd.to_datetime(
                            datetime.date(year, month, 1)
                        )
                        end_date = begin_date + DATE_OFFSET_TO_MONTH_END

                if not matched:
                    matched = DATE_RANGE_PATTERN.fullmatch(raw_string)
                    if matched:
                        begin_year = parse_date_component(
                            matched.group(1),
                            raw_value=raw_string,
                        )
                        begin_month = int(matched.group(2))
                        begin_day = int(matched.group(3))
                        end_year = parse_date_component(
                            matched.group(4),
                            default_value=begin_year,
                            raw_value=raw_string,
                        )
                        end_month = parse_date_component(
                            matched.group(5),
                            default_value=begin_month,
                            raw_value=raw_string,
                        )
                        end_day = int(matched.group(6))
                        begin_date = pd.to_datetime(
                            datetime.date(begin_year, begin_month, begin_day)
                        )
                        end_date = pd.to_datetime(
                            datetime.date(end_year, end_month, end_day)
                        )

                if not matched:
                    matched = MONTH_RANGE_PATTERN.fullmatch(raw_string)
                    if matched:
                        begin_year = parse_date_component(
                            matched.group(1),
                            raw_value=raw_string,
                        )
                        begin_month = int(matched.group(2))
                        end_year = parse_date_component(
                            matched.group(3),
                            default_value=begin_year,
                            raw_value=raw_string,
                        )
                        end_month = parse_date_component(
                            matched.group(4),
                            default_value=begin_month,
                            raw_value=raw_string,
                        )
                        begin_date = pd.to_datetime(
                            datetime.date(begin_year, begin_month, 1)
                        )
                        end_date = pd.to_datetime(
                            datetime.date(end_year, end_month, 1)
                        )
                        end_date += DATE_OFFSET_TO_MONTH_END

                if not matched:
                    if DATE_SEP_EN in raw_string:
                        sep_index = raw_string.index(DATE_SEP_EN)
                        begin_date = pd.to_datetime(raw_string[:sep_index])
                        end_date = pd.to_datetime(raw_string[(sep_index + 1):])
                    else:
                        begin_date = pd.to_datetime(raw_string)
                        end_date = begin_date

            except:
                raise ImportTableError(
                    f'无法识别的日期：{raw_value}'
                )

        index = df_result.index[i]
        df_result.loc[index, 'activity_begin'] = begin_date
        df_result.loc[index, 'activity_end'] = end_date
