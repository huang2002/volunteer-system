from ..common import *
from .common import *

# all extensions will be in lower case
ACCEPTABLE_EXCEL_EXTENSIONS = ('.xlsx')
ACCEPTABLE_CSV_EXTENSIONS = ('.csv', '.csv.gz')
ACCEPTABLE_TSV_EXTENSIONS = ('.tsv', '.tsv.gz')


def load_dataframe(
    file: FileStorage,
    *,
    skiprows=0,
    nrows=None,
) -> pd.DataFrame:

    filename = str(file.filename)
    filename_lower = filename.lower()

    common_params = {
        'skiprows': skiprows,
        'nrows': nrows,
        'parse_dates': False,
    }

    if filename_lower.endswith(ACCEPTABLE_EXCEL_EXTENSIONS):
        return pd.read_excel(file, **common_params)
    elif filename_lower.endswith(ACCEPTABLE_CSV_EXTENSIONS):
        return pd.read_csv(file, **common_params)
    elif filename_lower.endswith(ACCEPTABLE_TSV_EXTENSIONS):
        return pd.read_csv(file, **common_params, sep='\t')
    else:
        raise ImportTableError(f'无法识别的表格：{filename}')
