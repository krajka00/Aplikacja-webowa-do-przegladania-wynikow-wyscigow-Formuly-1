import os
import yaml
from WynikiF1.models import Circuit, Country

YAML_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'yaml_data', 'circuits')

def load_yaml(file_name):
    file_path = os.path.join(YAML_DIR, file_name)
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def import_circuits_data():
    if not os.path.exists(YAML_DIR):
        print(f"Ścieżka {YAML_DIR} nie istnieje")
        return

    for file_name in os.listdir(YAML_DIR):
        if file_name.endswith('.yml'):
            circuit_data = load_yaml(file_name)

            try:
                country = Country.objects.get(name__iexact=circuit_data['countryId'])
            except Country.DoesNotExist:
                print(f"Country with name '{circuit_data['countryId']}' does not exist. Skipping {file_name}.")
                continue

            Circuit.objects.get_or_create(
                name=circuit_data['name'],
                full_name=circuit_data['fullName'],
                circuit_type=circuit_data['type'],
                place_name=circuit_data['placeName'],
                country=country,
                latitude=circuit_data['latitude'],
                longitude=circuit_data['longitude']
            )
