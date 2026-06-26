import click
import functools

from auth.auth import decode_token


def validate_prompt(prompt, validate_function, optional=False, **kwargs):
    """Redemande le champ tant qu'il est invalide."""
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
    """Vérifie le rôle avant d'entrer dans la commande."""

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
