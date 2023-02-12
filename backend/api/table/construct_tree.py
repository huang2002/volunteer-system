from ..common import *
from .common import *

KEY_SEP = '-'
GRADE_NAME = 'grade'
TREE_COLUMNS = [
    'student_school',
    'student_class',
    'student_id',
]
TREE_LEVELS = [
    'student_school',
    GRADE_NAME,
    'student_class',
    'student_id',
]


def construct_tree() -> Any:

    table_names = get_table_names()

    dataframes = []
    for table_name in table_names:
        df = read_table(
            get_table_path(table_name),
            usecols=TREE_COLUMNS,
        )
        df[GRADE_NAME] = table_name
        dataframes.append(df)

    df_tree = pd.concat(dataframes, ignore_index=True)
    df_tree.drop_duplicates(inplace=True)
    df_tree.sort_values(by=TREE_LEVELS, inplace=True)

    result = []
    max_depth = len(TREE_LEVELS)
    key_path = [None] * max_depth
    node_path = [None] * max_depth

    for index in df_tree.index:
        for depth, level in enumerate(TREE_LEVELS):

            key = df_tree.loc[index, level]
            if key_path[depth] == key:
                continue

            key_path[depth] = key
            for i in range(depth + 1, max_depth):
                key_path[i] = None

            new_node = {
                'title': key,
                'key': KEY_SEP.join(
                    key_path[:(depth + 1)]
                ),
            }
            if depth != max_depth - 1:
                new_node['children'] = []
            node_path[depth] = new_node

            if depth == 0:
                result.append(new_node)
            else:
                node_path[depth - 1]['children'].append(new_node)

    return result
