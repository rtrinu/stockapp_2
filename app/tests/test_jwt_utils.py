import time
import jwt
import pytest

from datetime import datetime, timedelta

from backend.core.settings import settings
from backend.core.auth_handler import (
    create_access_token,
    create_refresh_token,
    decode_jwt,
    refresh_access_token,
)

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM


# ———————————————————————————————————————————————
#    Access Token: creation and structure tests
# ———————————————————————————————————————————————


def test_access_token_contains_expected_claims():
    token = create_access_token("user123")
    decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

    assert decoded["sub"] == "user123"
    assert decoded["type"] == "access"
    assert "exp" in decoded


def test_decode_jwt_returns_payload_on_valid_token():
    token = create_access_token("someuser")
    result = decode_jwt(token)
    assert isinstance(result, dict)
    assert result["sub"] == "someuser"


# ———————————————————————————————————————————————
#    Expiration behavior
# ———————————————————————————————————————————————


def test_decode_jwt_rejects_expired_token():
    # Create a token that expires immediately in the past
    exp = datetime.now().timestamp() - 1
    bad_token = jwt.encode(
        {"sub": "u", "type": "access", "exp": exp}, JWT_SECRET, algorithm=JWT_ALGORITHM
    )

    assert decode_jwt(bad_token) is None


def test_expiration_boundary():
    # Small time window token
    token = jwt.encode(
        {"sub": "boundary", "type": "access", "exp": datetime.now().timestamp() + 1},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    # Immediately valid
    assert isinstance(decode_jwt(token), dict)
    # After a slight delay it should be invalid
    time.sleep(1.1)
    assert decode_jwt(token) is None


# ———————————————————————————————————————————————
#    Tampering / invalid signature
# ———————————————————————————————————————————————


def test_tampered_signature_fails():
    token = create_access_token("attacker")
    parts = token.split(".")
    # Tamper payload base64 (simple invalid part)
    parts[1] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"  # fake base64 header
    tampered = ".".join(parts)

    assert decode_jwt(tampered) is None


def test_garbage_token_rejected():
    assert decode_jwt("not-a.token.at.all") is None


# ———————————————————————————————————————————————
#    Token Claims
# ———————————————————————————————————————————————


def test_missing_sub_claim_is_invalid():
    # No "sub" claim
    payload = {"type": "access", "exp": datetime.now().timestamp() + 60}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    decoded = decode_jwt(token)
    assert decoded is None


def test_wrong_type_claim_rejected_on_refresh():
    # Create an access token and try to use as refresh
    access = create_access_token("u")
    assert refresh_access_token(access) is None


# ———————————————————————————————————————————————
#    Refresh Token Behavior
# ———————————————————————————————————————————————


def test_refresh_token_contains_claims():
    r_token = create_refresh_token("ruser", "refresh-id-123")
    decoded = jwt.decode(r_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

    assert decoded["sub"] == "ruser"
    assert decoded["jti"] == "refresh-id-123"
    assert decoded["type"] == "refresh"
    assert "exp" in decoded


def test_refresh_access_token_generates_new_valid_token():
    r_token = create_refresh_token("refreshme", "tid555")
    new_atoken = refresh_access_token(r_token)

    assert new_atoken is not None
    new_payload = jwt.decode(new_atoken, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    assert new_payload["sub"] == "refreshme"
    assert new_payload["type"] == "access"


def test_refresh_token_expiry_prevents_new_token():
    # expired refresh token -> should be rejected
    exp = datetime.now().timestamp() - 1
    bad_refresh = jwt.encode(
        {"sub": "r", "type": "refresh", "jti": "t", "exp": exp},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )

    assert refresh_access_token(bad_refresh) is None


# ———————————————————————————————————————————————
#    Invalid / Bad Inputs
# ———————————————————————————————————————————————


def test_refresh_token_with_missing_jti():
    # missing jti means refresh logic should not generate a new token
    payload = {"sub": "some", "type": "refresh", "exp": datetime.now().timestamp() + 60}
    r_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    assert refresh_access_token(r_token) is None


def test_decode_jwt_raises_no_exception_on_bad():
    # no exception escapes
    assert decode_jwt(None) is None
    assert decode_jwt("") is None
