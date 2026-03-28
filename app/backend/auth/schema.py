from pydantic import BaseModel, EmailStr
from typing import Annotated
from fastapi import Form


class SignupData(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    client_key: str
    client_secret: str

    first_name: Annotated[str, Form(...)]
    last_name: Annotated[str, Form(...)]
    email: Annotated[EmailStr, Form(...)]
    password: Annotated[str, Form(...)]
    client_key: Annotated[str, Form(...)]
    client_secret: Annotated[str, Form(...)]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    email: Annotated[str, Form(...)]
    password: Annotated[str, Form(...)]
