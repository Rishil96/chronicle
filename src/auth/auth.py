import bcrypt
import jwt
import logging
from datetime import datetime, UTC, timedelta
from src.config import settings

# Create logger
logger = logging.getLogger("chronicle")

# Generate password hash
def hash_password(password: str) -> str:
    """
    This function hashes the given input password and returns the hashed password.
    """
    hashed_password = bcrypt.hashpw(password=password.encode("utf-8"), salt=bcrypt.gensalt())
    return hashed_password.decode("utf-8")

# Verify password
def verify_password(input_password: str, hashed_password: str) -> bool:
    """
    This function verifies the given input password and returns whether it is correct.
    """
    return bcrypt.checkpw(input_password.encode("utf-8"), hashed_password.encode("utf-8"))

# Create access token
def create_access_token(data: dict) -> str:
    """
    This function creates an access token given a dictionary containing information about the user.
    """
    data["exp"] = datetime.now(tz=UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    encoded_token = jwt.encode(payload=data, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_token

# Decode access token
def decode_access_token(token: str) -> dict | None:
    """
    This function decodes an access token given a jwt token.
    """
    try:
        decoded_data = jwt.decode(jwt=token, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        return decoded_data
    except jwt.ExpiredSignatureError as e:
        logger.error(f"The access token has been expired. Error message: {e}")
        return None
    except jwt.InvalidTokenError as e:
        logger.error(f"The access token is invalid. Error message: {e}")
        return None
