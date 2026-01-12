from datetime import datetime

ALLOWED_NAMES = {
    "test",
    "Admin"
}

def validate_token(token: str) -> tuple[bool, str]:
    if not token or len(token) < 8:
        return False, "Invalid token format"

    date_part = token[-8:]
    name = token[:-8]

    if name not in ALLOWED_NAMES:
        return False, "User not authorized"

    try:
        token_date = datetime.strptime(date_part, "%d%m%Y").date()
    except ValueError:
        return False, "Invalid date format"

    today = datetime.now().date()
    if token_date != today:
        return False, "Token date is not valid today"

    return True, name
