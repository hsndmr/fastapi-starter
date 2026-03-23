from app.core.security import generate_api_key


# @demo-code test generate api key
def test_generate_api_key() -> None:
    key = generate_api_key()
    assert isinstance(key, str)
    assert len(key) == 64


# @demo-code test generate api key uniqueness
def test_generate_api_key_unique() -> None:
    key1 = generate_api_key()
    key2 = generate_api_key()
    assert key1 != key2
