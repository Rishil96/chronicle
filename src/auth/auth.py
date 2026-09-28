import bcrypt


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
