import os
import yaml
from WynikiF1.models import TyreManufacturer, Country

YAML_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'yaml_data', 'tyre-manufacturers')

def load_yaml(file_name):
    """Funkcja wczytująca dane z pliku YAML."""
    file_path = os.path.join(YAML_DIR, file_name)
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def import_tyre_manufacturers_data():
    """Funkcja importująca dane producentów opon z plików YAML do bazy danych."""
    if not os.path.exists(YAML_DIR):
        print(f"Ścieżka {YAML_DIR} nie istnieje")
        return

    for file_name in os.listdir(YAML_DIR):
        if file_name.endswith('.yml'):
            manufacturer_data = load_yaml(file_name)

            try:
                country = Country.objects.get(name__iexact=manufacturer_data['countryId'])
            except Country.DoesNotExist:
                print(f"Country with name '{manufacturer_data['countryId']}' does not exist. Skipping {file_name}.")
                continue

            TyreManufacturer.objects.get_or_create(
                name=manufacturer_data['name'],
                country=country
            )
