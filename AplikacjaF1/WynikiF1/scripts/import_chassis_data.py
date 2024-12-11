import os
import yaml
from WynikiF1.models import Chassis, Constructor

YAML_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'yaml_data', 'chassis')

def load_yaml(file_name):
    file_path = os.path.join(YAML_DIR, file_name)
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def import_chassis_data():
    if not os.path.exists(YAML_DIR):
        print(f"Ścieżka {YAML_DIR} nie istnieje")
        return

    for file_name in os.listdir(YAML_DIR):
        if file_name.endswith('.yml'):
            chassis_data = load_yaml(file_name)

            try:
                constructor = Constructor.objects.get(name__iexact=chassis_data['constructorId'])
            except Constructor.DoesNotExist:
                print(f"Constructor with name '{chassis_data['constructorId']}' does not exist. Skipping {file_name}.")
                continue

            Chassis.objects.get_or_create(
                name=chassis_data['name'],
                full_name=chassis_data['fullName'],
                constructor=constructor
            )
