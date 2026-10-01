import os

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from .roles import ROLE_API_KEYS, Role

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

DEFAULT_API_KEY = os.getenv("ALERT_API_KEY", "dev-alert-key")
VALID_API_KEYS = {DEFAULT_API_KEY, *ROLE_API_KEYS.values()}


def get_api_key(api_key: str | None = Depends(api_key_header)) -> str:
    if api_key is None or api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return api_key


def get_role_from_api_key(api_key: str) -> Role:
    for role, key in ROLE_API_KEYS.items():
        if api_key == key:
            return role
    return Role.OPERATOR


def require_admin(api_key: str = Depends(get_api_key)) -> str:
    role = get_role_from_api_key(api_key)
    if role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return api_key
