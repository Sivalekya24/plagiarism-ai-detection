"""
Dependency to gate any admin-only route.

Usage in any router:

    from fastapi import APIRouter, Depends
    from app.api.deps import require_admin

    router = APIRouter()

    @router.get("/repository/documents", dependencies=[Depends(require_admin)])
    def list_documents():
        ...

Attach this to EVERY /repository/* and /code/documents, /code/statistics,
/code/document/{filename} route. The frontend hiding the admin tab/route is
just UX -- this dependency is the actual access control.
"""

from fastapi import Header, HTTPException, status

from auth.security import decode_admin_token


def require_admin(authorization: str | None = Header(default=None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing admin token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization.removeprefix("Bearer ").strip()
    try:
        return decode_admin_token(token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired admin token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
