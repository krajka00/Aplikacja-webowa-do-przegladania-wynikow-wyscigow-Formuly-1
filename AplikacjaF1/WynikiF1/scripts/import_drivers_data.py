import os
import yaml
from WynikiF1.models import Driver, Country

YAML_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'yaml_data', 'drivers')

def load_yaml(file_name):
    """Funkcja wczytująca dane z pliku YAML."""
    file_path = os.path.join(YAML_DIR, file_name)
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def import_drivers_data():
    """Funkcja importująca dane drivers z plików YAML do bazy danych."""
    if not os.path.exists(YAML_DIR):
        print(f"Ścieżka {YAML_DIR} nie istnieje")
        return

    for file_name in os.listdir(YAML_DIR):
        if file_name.endswith('.yml'):
            driver_data = load_yaml(file_name)

            try:
                country_of_birth = Country.objects.get(name__iexact=driver_data['countryOfBirthCountryId'])
            except Country.DoesNotExist:
                print(f"Country with name '{driver_data['countryOfBirthCountryId']}' does not exist. Skipping {file_name}.")
                continue

            try:
                nationality = Country.objects.get(name__iexact=driver_data['nationalityCountryId'])
            except Country.DoesNotExist:
                print(f"Country with name '{driver_data['nationalityCountryId']}' does not exist. Skipping {file_name}.")
                continue

            Driver.objects.get_or_create(
                first_name=driver_data['firstName'],
                last_name=driver_data['lastName'],
                full_name=driver_data['fullName'],
                abbreviation=driver_data['abbreviation'],
                permanent_number=driver_data['permanentNumber'],
                gender=driver_data['gender'],
                date_of_birth=driver_data['dateOfBirth'],
                date_of_death=driver_data['dateOfDeath'] if driver_data['dateOfDeath'] else None,
                place_of_birth=driver_data['placeOfBirth'],
                country_of_birth=country_of_birth,
                nationality=nationality
            )
