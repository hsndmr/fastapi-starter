import secrets


# @demo-code security module example
def generate_api_key() -> str:
    return secrets.token_hex(32)
