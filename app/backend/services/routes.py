from fastapi import APIRouter, Depends
from backend.services.tradingClient import get_alpaca_client
from backend.auth.dependencies import get_current_user

router = APIRouter(tags=["client"])
