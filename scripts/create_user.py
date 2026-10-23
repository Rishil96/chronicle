from getpass import getpass

from src.auth import hash_password
from src.db.db_session import SessionLocal
from src.db import Users
from src.service_layer import get_user_by_email


def main() -> None:
    """
    Main function to create a new user
    """
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    email = input("Email: ").strip()
    password = getpass("Password: ")
    confirm_password = getpass("Confirm password: ")

    if not all([first_name, last_name, email, password]):
        print("All fields are required.")
        return
    if password != confirm_password:
        print("Passwords do not match.")
        return

    with SessionLocal() as session:
        if get_user_by_email(session, email) is not None:
            print(f"A user with email {email} already exists.")
            return
        session.add(
            Users(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=hash_password(password),
            )
        )
        session.commit()

    print(f"User {first_name} {last_name} created successfully.")


if __name__ == "__main__":
    main()
