from ..common import *

__all__ = [
    'AliasMap',
    'AliasList',
    'AliasLists',
    'load_aliases',
    'get_alias_map',
    'update_alias_list',
    'delete_alias_list',
    'save_aliases',
]

AliasMap = Dict[str, str]  # alias -> name
AliasList = List[str]
AliasLists = Dict[str, AliasList]  # name -> [aliases...]

alias_maps: Dict[str, AliasMap] = {
    "school_map": {},
    # TODO: "class_map": {},
}
alias_list_map: Dict[str, AliasLists] = {}


def set_aliases(target_map: AliasMap, source: Any) -> NoReturn:

    assert isinstance(source, dict)
    assert all(
        isinstance(aliases, list)
        for aliases in source.values()
    )
    assert all(
        isinstance(alias, str)
        for alias in aliases
        for aliases in source.values()
    )

    for name, alias_list in source.items():
        target_map[name] = name
        for alias in alias_list:
            target_map[alias] = name


def load_aliases() -> NoReturn:

    source = json.load(ALIASES_PATH)
    assert isinstance(source, dict)

    for map_name, source_map in source.items():
        set_aliases(alias_maps[map_name], source_map)


def get_alias_map(map_name: str) -> AliasMap:
    return alias_maps[map_name]


def update_alias_list(
    map_name: str,
    list_name: str,
    alias_list: AliasList,
) -> NoReturn:
    alias_list_map[map_name][list_name] = list_name
    alias_maps[map_name] = dict(
        (alias, list_name)
        for alias in alias_list
    )
    save_aliases()


def delete_alias_list(map_name: str, list_name: str) -> NoReturn:
    del alias_list_map[map_name][list_name]
    del alias_maps[map_name][list_name]
    save_aliases()


def save_aliases() -> NoReturn:
    with open(ALIASES_PATH, 'w') as output_file:
        json.dump(alias_maps, output_file)
