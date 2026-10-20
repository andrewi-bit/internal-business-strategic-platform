from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

import jwt
import hashlib
import secrets

from app.settings import settings

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """Hash password sebelum disimpan ke database."""
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifikasi password terhadap hash yang tersimpan."""
    return password_hash.verify(password, hashed_password)

def create_access_token(
    subject: str,
    token_version: int = 0,
) -> str:
    """Create a signed JWT access token."""
    now = datetime.now(timezone.utc)

    payload = {
        "sub": subject,
        "ver": token_version,
        "iat": now,
        "exp": now + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token."""
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )

def create_refresh_token() -> str:
    """Generate a cryptographically secure opaque refresh token."""
    return secrets.token_urlsafe(64)

def hash_refresh_token(token: str) -> str:
    """Hash a refresh token before storing it in the database."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

def create_password_reset_token() -> str:
    """Generate a cryptographically secure password reset token."""
    return secrets.token_urlsafe(32)

def hash_password_reset_token(token: str) -> str:
    """Hash a password reset token before storing it in the database."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
