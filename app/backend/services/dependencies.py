from backend.auth.dependencies import get_current_user


def get_trading_client(user=Depends(get_current_user)):
    return get_alpaca_client(user)
