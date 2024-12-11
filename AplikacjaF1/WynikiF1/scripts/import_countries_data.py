import os
import yaml
from WynikiF1.models import Country, Continent

YAML_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'yaml_data', 'countries')

def load_yaml(file_name):
    file_path = os.path.join(YAML_DIR, file_name)
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def import_countries_data():
    if not os.path.exists(YAML_DIR):
        print(f"Ścieżka {YAML_DIR} nie istnieje")
        return

    for file_name in os.listdir(YAML_DIR):
        if file_name.endswith('.yml'):
            country_data = load_yaml(file_name)

            try:
                continent = Continent.objects.get(name__iexact=country_data['continentId'])
            except Continent.DoesNotExist:
                print(f"Continent with name '{country_data['continentId']}' does not exist. Skipping {file_name}.")
                continue

            Country.objects.get_or_create(
                name=country_data['name'],
                alpha2_code=country_data['alpha2Code'],
                alpha3_code=country_data['alpha3Code'],
                demonym=country_data['demonym'],
                continent=continent
            )
