import click
import functools

from auth.auth import decode_token


def validate_prompt(prompt, validate_function, optional=False, **kwargs):
    """
    Prompt user for input and re-ask until valid.

    Returns None if optional and input is empty.
    """
    while True:
        value = click.prompt(prompt, **kwargs)

        if isinstance(value, str):
            value = value.strip()

        if optional and (value is None or value == "" or value == 0.0):
            return None

        try:
            return validate_function(value)
        except ValueError as e:
            click.echo(click.style(f"{e}", fg="red"))


def require_cli_role(*allowed_roles):
    """
    CLI decorator that restricts command access to specified roles.

    Raises:
        PermissionError: If the token role is not in allowed_roles.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ctx = click.get_current_context()
            token = ctx.obj.get("token")
            if not token:
                click.echo(click.style("Vous devez être connecté.", fg="red"))
                return
            payload = decode_token(token)
            if payload.get("role") not in allowed_roles:
                click.echo(click.style(
                    f"Accès refusé. Rôle(s) autorisé(s) : {', '.join(allowed_roles)}.", fg="red"))
                return
            return func(*args, **kwargs)

        return wrapper

    return decorator
