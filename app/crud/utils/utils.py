from enum import Enum
from typing import Union, Sequence


def ensure_enums_to_strs(items: Sequence[Union[Enum, str]]):
    str_items = []
    for item in items:
        if isinstance(item, Enum):
            str_items.append(str(item.value))
        else:
            str_items.append(str(item))

    return str_items
