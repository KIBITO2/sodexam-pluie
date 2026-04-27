from pathlib import Path

APP_TITLE = "SODEXAM - Gestion Nationale"
PAGE_ICON = "🌧️"
LAYOUT = "wide"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Donnees_Villes"
ARCHIVE_DIR = BASE_DIR / "archives"
USERS_FILE = BASE_DIR / "utilisateurs.csv"
VILLES_FILE = BASE_DIR / "villes_ci.csv"
LOGO_FILE = BASE_DIR / "logo_sodexam.png"

SEUIL_ALERTE_MM = 50.0
SEUIL_VIGILANCE_MM = 20.0

PHENOMENES_OPTIONS = [
    "Aucun",
    "Pluie faible",
    "Pluie modérée",
    "Pluie forte",
    "Orage",
    "Brouillard",
    "Vent fort",
    "Ciel couvert",
]

ROLES_VALIDES = ["admin", "agent"]

COLONNES_UTILISATEURS = ["username", "password_hash", "role", "ville", "email"]
COLONNES_VILLES = ["Ville", "Latitude", "Longitude"]
COLONNES_RELEVE = [
    "id",
    "Date",
    "Heure",
    "Pluie_mm",
    "Phenomene",
    "Observation",
    "Agent",
    "Saisi_le",
]

DEFAULT_VILLES = [
    {"Ville": "Abidjan", "Latitude": 5.3364, "Longitude": -4.0267},
    {"Ville": "Bouaké", "Latitude": 7.6892, "Longitude": -5.0300},
    {"Ville": "Yamoussoukro", "Latitude": 6.8276, "Longitude": -5.2893},
    {"Ville": "San Pedro", "Latitude": 4.7485, "Longitude": -6.6363},
    {"Ville": "Korhogo", "Latitude": 9.4580, "Longitude": -5.6296},
    {"Ville": "Man", "Latitude": 7.4125, "Longitude": -7.5538},
    {"Ville": "Daloa", "Latitude": 6.8890, "Longitude": -6.4500},
    {"Ville": "Gagnoa", "Latitude": 6.1319, "Longitude": -5.9506},
    {"Ville": "Bondoukou", "Latitude": 8.0402, "Longitude": -2.8000},
    {"Ville": "Odienné", "Latitude": 9.5100, "Longitude": -7.5690},
    {"Ville": "Abengourou", "Latitude": 6.7297, "Longitude": -3.4964},
    {"Ville": "Divo", "Latitude": 5.8374, "Longitude": -5.3572},
]
