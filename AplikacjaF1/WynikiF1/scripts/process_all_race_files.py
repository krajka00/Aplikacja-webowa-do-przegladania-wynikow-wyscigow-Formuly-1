import os

RACES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'yaml_data', 'seasons', '2023', 'races')

def replace_dash_with_space_in_lines_with_id(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    for line in lines:
        if "Id" in line:
            modified_lines.append(line.replace('-', ' ', 1))
        else:
            modified_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(modified_lines)

def process_all_race_files():
    for race_folder in os.listdir(RACES_DIR):
        race_path = os.path.join(RACES_DIR, race_folder)
        if os.path.isdir(race_path):
            for file_name in os.listdir(race_path):
                if file_name.endswith('.yml'):
                    file_path = os.path.join(race_path, file_name)
                    replace_dash_with_space_in_lines_with_id(file_path)

if __name__ == "__main__":
    process_all_race_files()
