from pathlib import Path

TOKEN_FILE = Path(__file__).parent / ".crm_token"


def save_token(token):
    """Save JWT token to local file."""
    TOKEN_FILE.write_text(token)


def load_token() :
    """Load JWT token from local file. Returns None if not found."""
    if not TOKEN_FILE.exists():
        return None
    return TOKEN_FILE.read_text().strip()


def delete_token():

    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
