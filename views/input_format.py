from datetime import datetime

def input_date(prompt: str) -> datetime:
    format = "%d/%m/%Y"
    while True:
        saisie = input(prompt).strip()
        try:
            return datetime.strptime(saisie, format)
        except ValueError:
            print(f"Format invalide, veuillez saisir une date au format JJ/MM/AAAA")