"""
Run this once to generate the value for ADMIN_PASSWORD_HASH.

    python generate_admin_hash.py

It prompts for a password (hidden input) and prints the bcrypt hash.
Paste that hash -- never the raw password -- into your .env file.
"""

import getpass

import bcrypt

if __name__ == "__main__":
    password = getpass.getpass("Choose an admin password: ")
    confirm = getpass.getpass("Confirm: ")
    if password != confirm:
        raise SystemExit("Passwords didn't match -- nothing generated.")
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    print("\nADMIN_PASSWORD_HASH=" + hashed)
