import os
import yaml
from WynikiF1.models import Entrant

YAML_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'yaml_data', 'entrants')

def load_yaml(file_name):
    """Funkcja wczytująca dane z pliku YAML."""
    file_path = os.path.join(YAML_DIR, file_name)
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def import_entrants_data():
    """Funkcja importująca dane entrantów z plików YAML do bazy danych."""
    if not os.path.exists(YAML_DIR):
        print(f"Ścieżka {YAML_DIR} nie istnieje")
        return

    for file_name in os.listdir(YAML_DIR):
        if file_name.endswith('.yml'):
            entrant_data = load_yaml(file_name)

            Entrant.objects.get_or_create(
                name=entrant_data['name']
            )
