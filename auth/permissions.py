import functools
from auth.auth import decode_token


# C'est un décorateur paramétrable —
# une fonction qui retourne un décorateur, qui retourne une fonction.
# Trois niveaux d'imbrication car on a besoin de passer des paramètres (allowed_roles).
def require_role(*allowed_roles):  # capture tous les rôles passés en argument dans un tuple
    """Décorateur qui vérifie le rôle avant d'exécuter le contrôleur."""

    def decorator(func):  # func c'est la fonction décorée
        @functools.wraps(func)  # permet de conserver le nom et docstring de la fonction originale
        # *args, **kwargs transmettent tous les arguments éventuels à la vraie fonction sans les modifier.
        def wrapper(token: str, *args, **kwargs):  # remplace la fonction décorée
            payload = decode_token(token)  # Décode le token
            if payload.get("role") not in allowed_roles:  # verifie le role
                raise PermissionError(
                    f"Accès refusé. Rôles autorisés : {allowed_roles}"
                )
            return func(token, *args, **kwargs)  # execute la vrai fonction

        return wrapper

    return decorator
