from ..common import *
from ..table.common import *
from ..alias.common import handle_aliases
from .common import *

export_blueprint = Blueprint('export', __name__, url_prefix='/export')


@export_blueprint.post('/create/<level>')
def create(level: str) -> ResponseType:

    if not level in EXPORT_LEVELS:
        return RESPONSE_INVALID_LEVEL

    timestamp = time.strftime(EXPORT_TIME_FORMAT)
    export_dir = get_export_path(
        f'{timestamp}_{LEVEL_DISPLAY_NAMES[level]}'
    )
    if os.path.exists(export_dir):
        return RESPONSE_TOO_FREQUENT
    os.mkdir(export_dir)

    try:

        options = request.args

        if not KEY_SELECTED_TABLES in options:
            return RESPONSE_NO_TABLES_SELECTED
        selected_table_names = options[KEY_SELECTED_TABLES].split(',')
        all_table_names = get_table_names()
        if any(
            (not table_name in all_table_names)
            for table_name in selected_table_names
        ):
            return RESPONSE_INVALID_TABLE_NAME

        dataframes = []
        for table_name in selected_table_names:
            df = read_table(get_table_path(table_name))
            df[GRADE_COLUMN_NAME] = table_name
            dataframes.append(df)
        df_data = pd.concat(dataframes)
        handle_aliases(df_data)

        begin_date = None
        end_date = None
        if KEY_BEGIN_DATE in options:
            try:
                begin_date = convert_date(options[KEY_BEGIN_DATE])
            except:
                return RESPONSE_INVALID_DATA
            df_data = df_data.loc[
                df_data['activity_end'] >= begin_date
            ]
        if KEY_END_DATE in options:
            try:
                end_date = convert_date(options[KEY_END_DATE])
            except:
                return RESPONSE_INVALID_DATA
            df_data = df_data.loc[
                df_data['activity_begin'] <= end_date
            ]

        filename_suffix = ''
        if begin_date:
            begin_date_str = begin_date.strftime(EXPORT_DATE_FORMAT)
            if end_date:
                end_date_str = end_date.strftime(EXPORT_DATE_FORMAT)
                filename_suffix = f'_从{begin_date_str}到{end_date_str}'
            else:
                filename_suffix = f'_自{begin_date_str}起'
        elif end_date:
            end_date_str = end_date.strftime(EXPORT_DATE_FORMAT)
            filename_suffix = f'_截至{end_date_str}'

        prefix_depth = EXPORT_LEVELS.index(level)
        levels = EXPORT_LEVELS[:(prefix_depth + 1)]
        level_keys = [LEVEL_KEYS[level] for level in levels]
        grouper = level_keys[0] if len(level_keys) == 1 else level_keys

        for level_path, group in df_data.groupby(grouper):
            if not isinstance(level_path, tuple):
                level_path = (level_path,)

            if prefix_depth:
                path_prefix = '/'.join(level_path[:prefix_depth])
                export_path = os.path.join(export_dir, path_prefix)
                os.makedirs(export_path, exist_ok=True)
            else:
                export_path = export_dir

            filename = level_path[-1] + filename_suffix
            file_path = os.path.join(export_path, filename)
            export_table(
                group.drop(columns=[GRADE_COLUMN_NAME]),
                file_path,
                output_format=options.get('format'),
                encoding=options.get('encoding'),
                suffix_encoding=options.get('suffix_encoding'),
            )

    except ExportError as error:
        shutil.rmtree(export_dir)
        return (error.message, 400)

    except Exception as exception:
        shutil.rmtree(export_dir)
        raise exception

    return RESPONSE_SUCCESS


@export_blueprint.post('/show')
def show() -> ResponseType:
    program = 'explorer' if sys.platform.startswith('win') else 'open'
    path = os.path.normpath(EXPORT_DIR)
    command = program + ' ' + path
    subprocess.run(command, shell=True)
    return RESPONSE_SUCCESS
