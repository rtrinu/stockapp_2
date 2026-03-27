# from fastapi import APIRouter, HTTPException, Depends, Response, Form, Request
# from fastapi.responses import RedirectResponse
# from sqlmodel import Session
# from backend.db.database import get_db
# from backend.models.models import User
# from backend.core.settings import settings
# from backend.core.cryptography import encrypt, decrypt

# from pwdlib import PasswordHash
# from uuid import uuid4
# from backend.core.hashing import hash_token, verify_token

# import jwt
# from datetime import datetime, timedelta, timezone
# from backend.auth.db import revoke_refresh_token

# hasher = PasswordHash.recommended()

# router = APIRouter()


# def get_or_refresh_access_token(request: Request, response: Response, db: Session):
#     token = request.cookies.get("access_token")
#     if token:
#         try:
#             payload = jwt.decode(
#                 token,
#                 settings.JWT_SECRET,
#                 algorithms=[settings.JWT_ALGORITHM],
#                 options={"verify_exp": False},
#             )
#             exp = payload.get("exp")
#             if exp:
#                 if datetime.fromtimestamp(exp, timezone.utc) > datetime.now(
#                     timezone.utc
#                 ):
#                     return token
#         except jwt.InvalidTokenError:
#             pass
#         except jwt.ExpiredSignatureError:
#             pass

#     refresh_token = request.cookies.get("refresh_token")

#     if not refresh_token:
#         return None

#     valid_refresh_token = validate_or_revoke_refresh_token(request, db)
#     if not valid_refresh_token:
#         return None
#     new_access = refresh_access_token(refresh_token)
#     if not new_access:
#         return None

#     response.set_cookie(
#         key="access_token",
#         value=new_access,
#         httponly=True,
#         secure=True,
#         samesite="strict",
#         max_age=settings.JWT_EXPIRATION_MINUTES * 60,
#         path="/",
#     )
#     return new_access


# def get_current_user(
#     request: Request, response: Response, db: Session = Depends(get_db)
# ):
#     token = get_or_refresh_access_token(request, response, db)
#     if not token:
#         raise HTTPException(status_code=401)

#     user_id = decode_jwt(token).get("sub")
#     if not user_id:
#         raise HTTPException(status_code=401)
#     user = db.query(User).get(user_id)
#     return user


# @router.get("/delete-account")
# def delete_account(
#     response: Response,
#     db: Session = Depends(get_db),
#     user: User = Depends(get_current_user),
# ):
#     db.delete(user)
#     db.commit()

#     response.delete_cookie("access_token", path="/")
#     response.delete_cookie("refresh_token", path="/")
#     return {"message": "User deleted successfully"}


# def validate_or_revoke_refresh_token(request: Request, db: Session = Depends(get_db)):
#     if not token:
#         raise HTTPException(status_code=401, detail="No refresh token found")
#     is_token_valid = is_token_not_expired(token)
#     user_id = decode_jwt(token).get("sub")
#     if not user_id:
#         raise HTTPException(status_code=401, detail="Malformed refresh token")
#     if is_token_valid:
#         return True
#     else:
#         result = revoke_refresh_token(db, user_id)
#         return False
