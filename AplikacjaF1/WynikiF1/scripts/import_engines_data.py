import os
import yaml
from WynikiF1.models import Engine, EngineManufacturer

YAML_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'yaml_data', 'engines')

def load_yaml(file_name):
    """Funkcja wczytująca dane z pliku YAML."""
    file_path = os.path.join(YAML_DIR, file_name)
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def import_engines_data():
    """Funkcja importująca dane silników z plików YAML do bazy danych."""
    if not os.path.exists(YAML_DIR):
        print(f"Ścieżka {YAML_DIR} nie istnieje")
        return

    for file_name in os.listdir(YAML_DIR):
        if file_name.endswith('.yml'):
            engine_data = load_yaml(file_name)

            try:
                manufacturer = EngineManufacturer.objects.get(name__iexact=engine_data['engineManufacturerId'])
            except EngineManufacturer.DoesNotExist:
                print(f"EngineManufacturer with name '{engine_data['engineManufacturerId']}' does not exist. Skipping {file_name}.")
                continue

            Engine.objects.get_or_create(
                name=engine_data['name'],
                full_name=engine_data['fullName'],
                manufacturer=manufacturer,
                capacity=engine_data['capacity'],
                configuration=engine_data['configuration'],
                aspiration=engine_data['aspiration']
            )
