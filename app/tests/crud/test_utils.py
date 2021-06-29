

from app.crud.utils.utils import ensure_enums_to_strs
from app.models.role import RoleEnum

from app.tests.utils.utils import random_lower_string

def test_ensure_enums_to_strs() -> None:
    role_enum = RoleEnum.superuser

    just_string = random_lower_string()

    assert [str(role_enum.value)] == ensure_enums_to_strs([role_enum])
    assert [str(role_enum.value), just_string] == ensure_enums_to_strs([role_enum, just_string])