from collections.abc import Generator
from typing import Annotated, Any

from fastapi import Depends, HTTPException, Request


# @demo-code Yield dependency — open a resource, clean up after request
def get_connection() -> Generator[dict[str, Any], None, None]:
    conn = {"status": "open", "data": []}
    try:
        yield conn
    finally:
        conn["status"] = "closed"


# @demo-code Annotated dependency
ConnectionDep = Annotated[dict, Depends(get_connection)]


# @demo-code
def get_current_user_id(request: Request) -> int:
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing user id")
    return int(user_id)


# @demo-code
UserIdDep = Annotated[int, Depends(get_current_user_id)]
