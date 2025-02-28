from typing import Dict

from fastapi import APIRouter

router = APIRouter(prefix="/ping", tags=["ping_pong"])


@router.get("/", response_model=Dict)
def ping() -> Dict:
    return {"ping": "pong"}
