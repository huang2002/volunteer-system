from ..common import *

__all__ = [
    'AliasMap',
    'AliasList',
    'AliasLists',
    'load_aliases',
    'get_alias_lists',
    'update_alias_list',
    'delete_alias_list',
    'save_aliases',
    'handle_aliases',
]

ALIASES_ENCODING = 'utf-8'

AliasMap = Dict[str, str]  # alias -> name
AliasList = List[str]
AliasLists = Dict[str, AliasList]  # name -> [aliases...]

# col -> alias_map
alias_maps: Dict[str, AliasMap] = {
    "student_school": {},
    # TODO: "class_map": {},
}

# col -> alias_lists
alias_list_map: Dict[str, AliasLists] = {}


def set_aliases(target_map: AliasMap, source: Any) -> NoReturn:

    assert isinstance(source, dict)
    assert all(
        isinstance(aliases, list)
        and all(isinstance(alias, str) for alias in aliases)
        for aliases in source.values()
    )

    for name, alias_list in source.items():
        target_map[name] = name
        for alias in alias_list:
            target_map[alias] = name


def load_aliases() -> NoReturn:

    global alias_list_map

    with open(ALIASES_PATH, 'r', encoding=ALIASES_ENCODING) as input_file:
        alias_list_map = json.load(input_file)
    assert isinstance(alias_list_map, dict)

    for column_name, source_map in alias_list_map.items():
        set_aliases(alias_maps[column_name], source_map)


def get_alias_lists(column_name: str) -> AliasLists:
    return alias_list_map[column_name]


def update_alias_list(
    column_name: str,
    list_name: str,
    alias_list: AliasList,
) -> NoReturn:
    for old_alias in alias_list_map[column_name][list_name]:
        del alias_maps[column_name][old_alias]
    alias_list_map[column_name][list_name] = alias_list
    for new_alias in alias_list:
        alias_maps[column_name][new_alias] = list_name
    save_aliases()


def delete_alias_list(column_name: str, list_name: str) -> NoReturn:
    del alias_list_map[column_name][list_name]
    del alias_maps[column_name][list_name]
    save_aliases()


def save_aliases() -> NoReturn:
    with open(ALIASES_PATH, 'w', encoding=ALIASES_ENCODING) as output_file:
        json.dump(alias_list_map, output_file)


def handle_aliases(df: pd.DataFrame) -> NoReturn:
    for column_name in df.columns:
        if not column_name in alias_maps:
            continue
        alias_map = alias_maps[column_name]
        df[column_name] = df[column_name].map(
            lambda value: (
                alias_map[value]
                if value in alias_map
                else value
            )
        )
