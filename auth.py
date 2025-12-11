# auth.py

API_TOKEN = "MY_SECRET_TOKEN_123"  # isti token setujes u WP pluginu

def validate_token(token: str) -> bool:
    if not token:
        return False
    return token == API_TOKEN
