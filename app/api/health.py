from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.config import Settings, get_settings


router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str


@router.get("/health", response_model=HealthResponse)
def health(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="clauseiq-api",
        version=settings.app_version,
        environment=settings.app_env,
    )