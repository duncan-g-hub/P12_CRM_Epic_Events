import time
import bcrypt
import jwt
import pytest

from auth import auth as auth_module

SECRET_KEY = "test-secret-key-with-32-bytes-min"


@pytest.fixture(autouse=True)
def fixed_secret(monkeypatch):
    monkeypatch.setattr(auth_module, "SECRET_KEY", SECRET_KEY)


def make_collaborator(mocker):
    collaborator = mocker.MagicMock()
    collaborator.id = 1
    collaborator.email = "email@email.com"
    collaborator.password = bcrypt.hashpw("Password1".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    collaborator.role.name = "commercial"
    return collaborator


# login
def test_login_with_correct_credentials_returns_token_and_collaborator(mocker):
    mock_session = mocker.MagicMock()
    mock_query = mocker.MagicMock()

    collaborator = make_collaborator(mocker)

    mock_query.filter.return_value.first.return_value = collaborator
    mock_session.query.return_value = mock_query

    mocker.patch("database.get_session", return_value=mock_session)

    token, returned = auth_module.login(collaborator.email, "Password1")

    assert returned is collaborator


def test_login_with_unknown_email_raises_value_error(mocker):
    mock_session = mocker.MagicMock()
    mock_query = mocker.MagicMock()

    mock_query.filter.return_value.first.return_value = None
    mock_session.query.return_value = mock_query

    mocker.patch("database.get_session", return_value=mock_session)

    with pytest.raises(ValueError):
        auth_module.login("unknown@test.com", "whatever")


def test_login_with_wrong_password_raises_value_error(mocker):
    mock_session = mocker.MagicMock()
    mock_query = mocker.MagicMock()

    collaborator = make_collaborator(mocker)

    mock_query.filter.return_value.first.return_value = collaborator
    mock_session.query.return_value = mock_query

    mocker.patch("database.get_session", return_value=mock_session)

    with pytest.raises(ValueError):
        auth_module.login(collaborator.email, "WrongPass1")


# decode_token
def test_decode_token_with_valid_token_returns_payload():
    token = jwt.encode({"id": 1, "role": "gestion", "exp": int(time.time()) + 3600},
                       SECRET_KEY, algorithm="HS256")

    payload = auth_module.decode_token(token)

    assert payload["id"] == 1
    assert payload["role"] == "gestion"


def test_decode_token_with_expired_token_raises_permission_error():
    token = jwt.encode({"id": 1, "role": "gestion", "exp": int(time.time()) - 10},
                       SECRET_KEY, algorithm="HS256")

    with pytest.raises(PermissionError):
        auth_module.decode_token(token)


def test_decode_token_with_wrong_token_raises_permission_error():
    with pytest.raises(PermissionError):
        auth_module.decode_token("wrong-token")
