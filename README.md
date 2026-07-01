# Epic Events CRM

Projet réalisé dans le cadre du développement d'une application CRM pour la société Epic Events
Application CRM en ligne de commande pour la gestion des collaborateurs, clients, contrats et événements.

---

## Fonctionnalités
- Authentification JWT (connexion)
- Gestion de permissions par rôle
- Création, modification, affichage :
  - Collaborateurs
  - Clients
  - Contrats
  - Événements
- Interactions avec l'application via CLI click

---

## Architecture
L'application suit une architecture MVC (modeles, vues, contrôlleurs), avec une couche supplémentaire pour la partie CLI.

---

## Structure du projet
```
auth/
    auth.py            # Authentification JWT
    permissions.py     # Décorateur de contrôle des rôles
    
commands/
    auth.py            # Commandes login / logout
    collaborators.py   # Commandes CLI collaborateurs
    customers.py       # Commandes CLI clients
    contracts.py       # Commandes CLI contrats
    events.py          # Commandes CLI événements
    utils.py           # Utilitaires CLI
    
controllers/
    collaborators.py   # Logique métier collaborateurs
    customers.py       # Logique métier clients
    contracts.py       # Logique métier contrats
    events.py          # Logique métier événements
    
models/
    models.py          # Modèles SQLAlchemy
    
views/
    views.py           # Fonctions d'affichage console
    
validators.py          # Validation des entrées
database.py            # Configuration de la base de données
token_storage.py       # Stockage local du token JWT
init_db.py             # Script pour l'initialisation de la BDD
main.py                # Point d'entrée de l'application
.env                   # Variables d'environnement (non committé)
```

---

## Technologies utilisées
- Python
- MySQL (BDD)
- SQLAlchemy (ORM)
- Click (CLI)
- PyJWT (Token)
- Bcrypt (Hachage mot de passe)
- Sentry (Journalisation)
- Flake8 (Linter)

---

## Installation

### Prérequis
- Python 3.10+
- Base de données MySQL


### Cloner le repository
```bash
   git clone https://github.com/duncan-g-hub/P12_CRM_Epic_Events
   cd P12_CRM_Epic_Events
```

### Créer et activer un environnement virtuel
```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS/Linux
```

### Installer les dépendances
```bash
   pip install -r requirements.txt
```

### Créer la base de données MySQL

Se connecter à MySQL avec un utilisateur root :
```bash
mysql -u root -p
```

Puis créer la base de données et un utilisateur dédié :
```sql
CREATE DATABASE epic_events_CRM CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON epic_events_CRM.* TO 'user'@'localhost';
EXIT;
```

### Configurer les variables d'environnement

Créer un fichier `.env` à la racine du projet :
```env
   DB_URL=mysql+mysqlconnector://'user':'password'@'localhost'/epic_events_CRM
   SECRET_KEY=votre_clé_secrète
   SENTRY_DSN=votre_sentry_dsn
```

### Initialiser la base de données
Les tables et les rôles sont créés automatiquement au premier lancement :
```bash
   python main.py --help
```

### Créer le compte administrateur
```bash
   python init_db.py
```
Identifiants par défaut : `admin@crm.com` / `Admin12345`

---

## Utilisation

```bash
python main.py [COMMANDE]
```

### Authentification
| Commande   | Description           |
|------------|-----------------------|
| `login`    | Se connecter au CRM   |
| `logout`   | Se déconnecter du CRM |

### Commandes disponibles
| Commande                | Description               | Rôles autorisés     |
|-------------------------|---------------------------|---------------------|
| `collaborators create`  | Créer un collaborateur    | gestion             |
| `collaborators update`  | Modifier un collaborateur | gestion             |
| `collaborators display` | Afficher un collaborateur | tous                |
| `customers create`      | Créer un client           | commercial          |
| `customers update`      | Modifier un client        | commercial, gestion |
| `customers display`     | Afficher un client        | tous                |
| `contracts create`      | Créer un contrat          | gestion             |
| `contracts update`      | Modifier un contrat       | commercial, gestion |
| `contracts display`     | Afficher un contrat       | tous                |
| `events create`         | Créer un événement        | commercial          |
| `events update`         | Modifier un événement     | gestion, support    |
| `events display`        | Afficher un événement     | tous                |

---

## Schéma de la base de données

Schéma UML des tables de la base de donnée :
![UML CRM.drawio.png](UML%20CRM.drawio.png)
---

## Rôles et permissions

| Rôle       | Permissions                                                                        |
|------------|------------------------------------------------------------------------------------|
| gestion    | Gérer les collaborateurs, créer des contrats, assigner des supports aux événements |
| commercial | Gérer ses propres clients, modifier ses propres contrats, créer des événements     |
| support    | Modifier les événements qui lui sont assignés                                      |

---

## Surveillance

Les exceptions inattendues et les actions métier clés sont suivies via Sentry :
- Toutes les exceptions inattendues
- Création et modification de collaborateurs
- Signature d'un contrat

---

## Contact

Pour toute question :  
Duncan GAURAT - duncan.dev@outlook.fr
