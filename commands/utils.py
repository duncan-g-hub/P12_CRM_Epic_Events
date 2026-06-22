import click

def validate_prompt(prompt, validate_function, optional=False, **kwargs):
    """Redemande le champ tant qu'il est invalide."""
    while True:
        value = click.prompt(prompt, **kwargs)

        if optional and not value.strip():
            return None

        try:
            return validate_function(value)
        except ValueError as e:
            click.echo(click.style(f"{e}", fg="red"))