from fastapi import APIRouter
from typing import Dict

router = APIRouter(prefix="/ping", tags=["ping_pong"])


@router.get("/", response_model=Dict)
def ping() -> Dict:
    return {"ping": "pong"}
