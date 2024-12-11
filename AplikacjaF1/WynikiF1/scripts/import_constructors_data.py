import os
import yaml
from WynikiF1.models import Constructor, Country

YAML_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'yaml_data', 'constructors')

def load_yaml(file_name):
    file_path = os.path.join(YAML_DIR, file_name)
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def import_constructors_data():
    if not os.path.exists(YAML_DIR):
        print(f"Ścieżka {YAML_DIR} nie istnieje")
        return

    for file_name in os.listdir(YAML_DIR):
        if file_name.endswith('.yml'):
            constructor_data = load_yaml(file_name)

            try:
                country = Country.objects.get(name__iexact=constructor_data['countryId'])
            except Country.DoesNotExist:
                print(f"Country with name '{constructor_data['countryId']}' does not exist. Skipping {file_name}.")
                continue

            Constructor.objects.get_or_create(
                name=constructor_data['name'],
                full_name=constructor_data['fullName'],
                country=country
            )
