from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    OPERATOR = "operator"


ROLE_API_KEYS = {
    Role.ADMIN: "admin-key",
    Role.OPERATOR: "operator-key",
}
