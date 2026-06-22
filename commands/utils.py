import click

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