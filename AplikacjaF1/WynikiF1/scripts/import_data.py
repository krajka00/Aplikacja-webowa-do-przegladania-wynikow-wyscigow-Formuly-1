import os
import yaml
from datetime import datetime


from WynikiF1.models import (Race, Driver, Constructor, EngineManufacturer, TyreManufacturer, StartingGrid,
                             RaceResult, DriverStanding, ConstructorStanding, FastestLap, PitStop, PracticeSession,
                             SprintQualifyingResult, SprintRaceResult, SprintStartingGrid, QualifyingResult)

base_path = r"C:\Users\jagua\Desktop\pwr\INFORMATYKA\Praca inżynierska\aplikacja\Aplikacja-webowa-do-przegladania-wynikow-wyscigow-Formuly-1\AplikacjaF1\WynikiF1\yaml_data\seasons\2023\races"

def load_yaml_data(file_path):
    print(f"Ładowanie danych z pliku: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def get_race(season, round):
    print(f"Pobieranie wyścigu dla sezonu {season}, runda {round}")
    return Race.objects.filter(season=season, round=round).first()

def get_driver(driver_id):
    print(f"Pobieranie kierowcy o ID: {driver_id}")
    driver_name_parts = driver_id.split()
    first_name = driver_name_parts[0]
    last_name = " ".join(driver_name_parts[1:])
    driver = Driver.objects.filter(first_name__iexact=first_name, last_name__iexact=last_name).first()
    if not driver:
        print(f"Nie znaleziono kierowcy: {driver_id}")
    return driver

def get_constructor(constructor_id):
    print(f"Pobieranie konstruktora o ID: {constructor_id}")
    constructor = Constructor.objects.filter(name__iexact=constructor_id).first()
    if not constructor:
        print(f"Nie znaleziono konstruktora: {constructor_id}")
    return constructor

def get_engine_manufacturer(engine_manufacturer_id):
    print(f"Pobieranie producenta silnika o ID: {engine_manufacturer_id}")
    engine_manufacturer = EngineManufacturer.objects.filter(name__iexact=engine_manufacturer_id).first()
    if not engine_manufacturer:
        print(f"Nie znaleziono producenta silnika: {engine_manufacturer_id}")
    return engine_manufacturer

def get_tyre_manufacturer(tyre_manufacturer_id):
    print(f"Pobieranie producenta opon o ID: {tyre_manufacturer_id}")
    tyre_manufacturer = TyreManufacturer.objects.filter(name__iexact=tyre_manufacturer_id).first()
    if not tyre_manufacturer:
        print(f"Nie znaleziono producenta opon: {tyre_manufacturer_id}")
    return tyre_manufacturer

def import_starting_grid(race, file_path):
    print(f"Importowanie Starting Grid dla wyścigu: {race}")
    data = load_yaml_data(file_path)
    for entry in data:
        print(f"Przetwarzanie pozycji: {entry}")
        driver = get_driver(entry['driverId'])

        if driver:
            position = entry['position']
            if position == 'PL':
                position = 0

            StartingGrid.objects.update_or_create(
                race=race,
                driver=driver,
                defaults={
                    'position': position
                }
            )
            print(f'Pozycja startowa dla kierowcy {driver} została dodana/zaktualizowana.')
        else:
            print(f'Nie udało się znaleźć wszystkich powiązanych obiektów dla pozycji: {entry}')

def import_race_results(race, file_path):
    print(f"Importowanie wyników wyścigu dla wyścigu: {race}")
    data = load_yaml_data(file_path)
    for entry in data:
        print(f"Przetwarzanie wyniku: {entry}")
        driver = get_driver(entry['driverId'])
        constructor = get_constructor(entry['constructorId'])
        if driver and constructor:
            position = entry['position']
            if position == 'DNF':
                position = 0
            elif position == 'DNS':
                position = 99
            elif position == 'DSQ':
                position = 999

            RaceResult.objects.update_or_create(
                race=race,
                driver=driver,
                constructor=constructor,
                defaults={
                    'position': position,
                    'points': entry['points'] if entry['points'] is not None else 0,
                    'laps': entry['laps'],
                    'time': entry.get('time', None),
                    'time_penalty': entry.get('timePenalty', None),
                    'gap': entry.get('gap', None),
                    'interval': entry.get('interval', None),
                    'reason_retired': entry.get('reasonRetired', None)
                }
            )
            print(f'Wynik wyścigu dla kierowcy {driver} został dodany/zaktualizowany.')
        else:
            print(f'Nie udało się znaleźć kierowcy lub konstruktora dla wyniku: {entry}')

def import_constructor_standings(race, file_path):
    print(f"Importowanie standings konstruktorów dla wyścigu: {race}")
    data = load_yaml_data(file_path)
    for entry in data:
        print(f"Przetwarzanie standings: {entry}")
        constructor = get_constructor(entry['constructorId'])
        if constructor:
            ConstructorStanding.objects.update_or_create(
                race=race,
                constructor=constructor,
                defaults={
                    'position': entry['position'],
                    'points': entry['points']
                }
            )
            print(f'Standing konstruktora {constructor} został dodany/zaktualizowany.')
        else:
            print(f'Nie udało się znaleźć konstruktora dla standings: {entry}')

def import_driver_standings(race, file_path):
    print(f"Importowanie standings kierowców dla wyścigu: {race}")
    data = load_yaml_data(file_path)
    for entry in data:
        print(f"Przetwarzanie standings: {entry}")
        driver = get_driver(entry['driverId'])
        if driver:
            DriverStanding.objects.update_or_create(
                race=race,
                driver=driver,
                defaults={
                    'position': entry['position'],
                    'points': entry['points']
                }
            )
            print(f'Standing kierowcy {driver} został dodany/zaktualizowany.')
        else:
            print(f'Nie udało się znaleźć kierowcy dla standings: {entry}')

def import_fastest_laps(race, file_path):
    print(f"Importowanie najszybszych okrążeń dla wyścigu: {race}")
    data = load_yaml_data(file_path)
    for entry in data:
        print(f"Przetwarzanie najszybszego okrążenia: {entry}")
        driver = get_driver(entry['driverId'])
        if driver:
            FastestLap.objects.update_or_create(
                race=race,
                driver=driver,
                defaults={
                    'lap': entry['lap'],
                    'lap_time': entry['time'],
                    'gap': entry.get('gap', None),
                    'interval': entry.get('interval', None)
                }
            )
            print(f'Najszybsze okrążenie dla kierowcy {driver} zostało dodane/zaktualizowane.')
        else:
            print(f'Nie udało się znaleźć kierowcy dla najszybszego okrążenia: {entry}')

def import_pit_stops(race, file_path):
    print(f"Importowanie pit stopów dla wyścigu: {race}")
    data = load_yaml_data(file_path)
    for entry in data:
        print(f"Przetwarzanie pit stopu: {entry}")
        driver = get_driver(entry['driverId'])
        if driver:
            PitStop.objects.update_or_create(
                race=race,
                driver=driver,
                stop_number=entry['stop'],
                defaults={
                    'lap': entry['lap'],
                    'duration': entry['time'],
                }
            )
            print(f'Pit stop dla kierowcy {driver} został dodany/zaktualizowany.')
        else:
            print(f'Nie udało się znaleźć kierowcy dla pit stopu: {entry}')

def import_practice_sessions(race, file_path, session_number):
    print(f"Importowanie wyników sesji treningowej (Practice {session_number}) dla wyścigu: {race}")
    data = load_yaml_data(file_path)
    for entry in data:
        print(f"Przetwarzanie wyniku sesji treningowej: {entry}")
        driver = get_driver(entry['driverId'])
        constructor = get_constructor(entry['constructorId'])
        if driver and constructor:
            PracticeSession.objects.update_or_create(
                race=race,
                driver=driver,
                session_number=session_number,
                defaults={
                    'constructor': constructor,
                    'position': entry['position'],
                    'time': entry.get('time', None),
                    'laps': entry.get('laps', None),
                    'gap': entry.get('gap', None),
                    'interval': entry.get('interval', None)
                }
            )
            print(f'Wynik sesji treningowej dla kierowcy {driver} został dodany/zaktualizowany.')
        else:
            print(f'Nie udało się znaleźć kierowcy lub konstruktora dla wyniku sesji treningowej: {entry}')

def import_sprint_qualifying(race, file_path):
    print(f"Importowanie wyników kwalifikacji sprintu dla wyścigu: {race}")
    data = load_yaml_data(file_path)
    for entry in data:
        print(f"Przetwarzanie wyniku kwalifikacji sprintu: {entry}")
        driver = get_driver(entry['driverId'])
        constructor = get_constructor(entry['constructorId'])
        if driver and constructor:
            position = entry['position']
            if position == 'DNF':
                position = 0
            elif position == 'DNS':
                position = 99
            elif position == 'DSQ':
                position = 999
            laps = entry.get('laps', 0)
            SprintQualifyingResult.objects.update_or_create(
                race=race,
                driver=driver,
                defaults={
                    'constructor': constructor,
                    'position': position,
                    'q1_time': entry.get('q1', None),
                    'q2_time': entry.get('q2', None),
                    'q3_time': entry.get('q3', None),
                    'laps': laps,
                    'gap': entry.get('gap', None),
                    'interval': entry.get('interval', None)
                }
            )
            print(f'Wynik kwalifikacji sprintu dla kierowcy {driver} został dodany/zaktualizowany.')
        else:
            print(f'Nie udało się znaleźć kierowcy dla wyniku kwalifikacji sprintu: {entry}')

def import_sprint_race(race, file_path):
    print(f"Importowanie wyników wyścigu sprintowego dla wyścigu: {race}")
    data = load_yaml_data(file_path)
    for entry in data:
        print(f"Przetwarzanie wyniku wyścigu sprintowego: {entry}")
        driver = get_driver(entry['driverId'])
        constructor = get_constructor(entry['constructorId'])
        if driver and constructor:
            position = entry['position']
            if position == 'DNF':
                position = 0
            elif position == 'DNS':
                position = 99
            elif position == 'DSQ':
                position = 999
            points = entry.get('points', 0)
            if points is None:
                points = 0
            laps = entry.get('laps', 0)
            SprintRaceResult.objects.update_or_create(
                race=race,
                driver=driver,
                constructor=constructor,
                defaults={
                    'position': position,
                    'points': points,
                    'laps': laps,
                    'time': entry.get('time', None),
                    'time_penalty': entry.get('timePenalty', None),
                    'gap': entry.get('gap', None),
                    'interval': entry.get('interval', None),
                    'reason_retired': entry.get('reasonRetired', None)
                }
            )
            print(f'Wynik sprintu dla kierowcy {driver} został dodany/zaktualizowany.')
        else:
            print(f'Nie udało się znaleźć kierowcy lub konstruktora dla wyniku sprintu: {entry}')

def import_sprint_starting_grid(race, file_path):
    print(f"Importowanie pozycji startowych sprintu dla wyścigu: {race}")
    data = load_yaml_data(file_path)
    for entry in data:
        print(f"Przetwarzanie pozycji startowej sprintu: {entry}")
        driver = get_driver(entry['driverId'])
        position = entry['position']
        if position == 'PL':
            position = 0
        if driver:
            SprintStartingGrid.objects.update_or_create(
                race=race,
                driver=driver,
                defaults={
                    'position': position
                }
            )
            print(f'Pozycja startowa sprintu dla kierowcy {driver} została dodana/zaktualizowana.')
        else:
            print(f'Nie udało się znaleźć kierowcy dla pozycji startowej sprintu: {entry}')

def import_qualifying(race, file_path):
    print(f"Importowanie wyników kwalifikacji dla wyścigu: {race}")
    data = load_yaml_data(file_path)
    for entry in data:
        print(f"Przetwarzanie wyniku kwalifikacji: {entry}")
        driver = get_driver(entry['driverId'])
        constructor = get_constructor(entry['constructorId'])
        if driver and constructor:
            position = entry['position']
            if position == 'DNF':
                position = 0
            elif position == 'DNS':
                position = 99
            elif position == 'DSQ':
                position = 999
            elif position == 'NC':
                position = 99
            points = entry.get('points', 0)
            if points is None:
                points = 0
            laps = entry.get('laps', 0)
            QualifyingResult.objects.update_or_create(
                race=race,
                driver=driver,
                defaults={
                    'constructor': constructor,
                    'position': position,
                    'q1_time': entry.get('q1', None),
                    'q2_time': entry.get('q2', None),
                    'q3_time': entry.get('q3', None),
                    'laps': laps,
                    'gap': entry.get('gap', None),
                    'interval': entry.get('interval', None)
                }
            )
            print(f'Wynik kwalifikacji dla kierowcy {driver} został dodany/zaktualizowany.')
        else:
            print(f'Nie udało się znaleźć kierowcy dla wyniku kwalifikacji: {entry}')

def import_all_data():
    for race_folder in os.listdir(base_path):
        race_path = os.path.join(base_path, race_folder)
        if os.path.isdir(race_path):
            season = 2023
            round_number = int(race_folder.split('-')[0])
            race = get_race(season=season, round=round_number)
            if not race:
                print(f'Wyścig dla folderu {race_folder} nie został znaleziony.')
                continue

            for session_num in range(1, 4):
                practice_session_path = os.path.join(race_path, f'free-practice-{session_num}-results.yml')
                if os.path.isfile(practice_session_path):
                    import_practice_sessions(race, practice_session_path, session_number=session_num)
            qualifying_path = os.path.join(race_path, 'qualifying-results.yml')
            if os.path.isfile(qualifying_path):
                import_qualifying(race, qualifying_path)

            sprint_qualifying_path = os.path.join(race_path, 'sprint-qualifying-results.yml')
            if os.path.isfile(sprint_qualifying_path):
                import_sprint_qualifying(race, sprint_qualifying_path)

            sprint_race_path = os.path.join(race_path, 'sprint-race-results.yml')
            if os.path.isfile(sprint_race_path):
                import_sprint_race(race, sprint_race_path)
            
            sprint_starting_grid_path = os.path.join(race_path, 'sprint-starting-grid-positions.yml')
            if os.path.isfile(sprint_starting_grid_path):
                import_sprint_starting_grid(race, sprint_starting_grid_path)

            starting_grid_path = os.path.join(race_path, 'starting-grid-positions.yml')
            if os.path.isfile(starting_grid_path):
                import_starting_grid(race, starting_grid_path)

            race_results_path = os.path.join(race_path, 'race-results.yml')
            if os.path.isfile(race_results_path):
                import_race_results(race, race_results_path)

            constructor_standings_path = os.path.join(race_path, 'constructor-standings.yml')
            if os.path.isfile(constructor_standings_path):
                import_constructor_standings(race, constructor_standings_path)

            driver_standings_path = os.path.join(race_path, 'driver-standings.yml')
            if os.path.isfile(driver_standings_path):
                import_driver_standings(race, driver_standings_path)

            fastest_laps_path = os.path.join(race_path, 'fastest-laps.yml')
            if os.path.isfile(fastest_laps_path):
                import_fastest_laps(race, fastest_laps_path)

            pit_stops_path = os.path.join(race_path, 'pit-stops.yml')
            if os.path.isfile(pit_stops_path):
                import_pit_stops(race, pit_stops_path)

if __name__ == "__main__":
    import_all_data()
