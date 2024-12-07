from django.test import TestCase
from WynikiF1.models import (
    Continent, Country, Constructor, Circuit, Driver, Race,
    DriverStanding, ConstructorStanding, RaceResult, Comment, FastestLap, PracticeSession,
    SprintQualifyingResult, SprintRaceResult, QualifyingResult
)
from django.contrib.auth.models import User
from datetime import date, datetime

class ContinentModelTest(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(code="EU", name="Europe", demonym="European")

    def test_continent_creation(self):
        self.assertEqual(self.continent.code, "EU")
        self.assertEqual(str(self.continent), "Europe")

class CountryModelTest(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(code="EU", name="Europe", demonym="European")
        self.country = Country.objects.create(
            name="Poland", alpha2_code="PL", alpha3_code="POL", demonym="Polish", continent=self.continent
        )

    def test_country_creation(self):
        self.assertEqual(self.country.name, "Poland")
        self.assertEqual(self.country.alpha2_code, "PL")
        self.assertEqual(str(self.country), "Poland")

class ConstructorModelTest(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(code="EU", name="Europe", demonym="European")
        self.country = Country.objects.create(
            name="Germany", alpha2_code="DE", alpha3_code="DEU", demonym="German", continent=self.continent
        )
        self.constructor = Constructor.objects.create(
            name="Mercedes", full_name="Mercedes AMG Petronas", country=self.country
        )

    def test_constructor_creation(self):
        self.assertEqual(self.constructor.name, "Mercedes")
        self.assertEqual(str(self.constructor), "Mercedes AMG Petronas (Mercedes)")

class CircuitModelTest(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(code="EU", name="Europe", demonym="European")
        self.country = Country.objects.create(
            name="Monaco", alpha2_code="MC", alpha3_code="MCO", demonym="Monégasque", continent=self.continent
        )
        self.circuit = Circuit.objects.create(
            name="Monte Carlo", full_name="Circuit de Monaco", circuit_type="Street",
            place_name="Monte Carlo", country=self.country, latitude=43.7347, longitude=7.4206
        )

    def test_circuit_creation(self):
        self.assertEqual(self.circuit.name, "Monte Carlo")
        self.assertEqual(str(self.circuit), "Circuit de Monaco (Monte Carlo)")

class DriverModelTest(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(code="EU", name="Europe", demonym="European")
        self.country = Country.objects.create(
            name="Netherlands", alpha2_code="NL", alpha3_code="NLD", demonym="Dutch", continent=self.continent
        )
        self.driver = Driver.objects.create(
            first_name="Max", last_name="Verstappen", abbreviation="VER",
            permanent_number=33, gender="Male", date_of_birth="1997-09-30",
            place_of_birth="Hasselt", country_of_birth=self.country, nationality=self.country
        )

    def test_driver_creation(self):
        self.assertEqual(self.driver.first_name, "Max")
        self.assertEqual(self.driver.permanent_number, 33)
        self.assertEqual(str(self.driver), "Max Verstappen")

class RaceModelTest(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(code="EU", name="Europe", demonym="European")
        self.country = Country.objects.create(
            name="Italy", alpha2_code="IT", alpha3_code="ITA", demonym="Italian", continent=self.continent
        )
        self.circuit = Circuit.objects.create(
            name="Monza", full_name="Autodromo Nazionale Monza", circuit_type="Permanent",
            place_name="Monza", country=self.country, latitude=45.6182, longitude=9.2818
        )
        self.race = Race.objects.create(
            season=2023, round=14, date="2023-09-03", official_name="Italian Grand Prix",
            qualifying_format="Standard", circuit=self.circuit, course_length=5.793, laps=53, distance=306.72
        )

    def test_race_creation(self):
        self.assertEqual(self.race.season, 2023)
        self.assertEqual(str(self.race), "Italian Grand Prix - 2023")

class CommentModelTest(TestCase):
    def setUp(self):
        # Tworzenie użytkownika
        self.user = User.objects.create_user(username="test_user", password="testpassword")
        
        self.continent = Continent.objects.create(code="EU", name="Europe", demonym="European")
        
        self.country = Country.objects.create(
            name="Italy", alpha2_code="IT", alpha3_code="ITA", demonym="Italian", continent=self.continent
        )
        
        self.circuit = Circuit.objects.create(
            name="Monza", full_name="Autodromo Nazionale Monza", circuit_type="Permanent",
            place_name="Monza", country=self.country, latitude=45.6182, longitude=9.2818
        )
        
        self.race = Race.objects.create(
            season=2023, round=14, date="2023-09-03", official_name="Italian Grand Prix",
            qualifying_format="Standard", circuit=self.circuit, course_length=5.793, laps=53, distance=306.72
        )
        
        self.comment = Comment.objects.create(
            race=self.race, 
            user=self.user, 
            content="Great race!"
        )
        
        self.comment.timestamp = datetime(2023, 9, 3, 15, 0, 0)
        self.comment.save()

    def test_comment_creation(self):
        self.assertEqual(self.comment.content, "Great race!")
        
        self.assertEqual(
            str(self.comment), 
            "test_user - Italian Grand Prix - 2023-09-03 15:00:00"
        )

class DriverModelTest(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(
            code="EU", name="Europe", demonym="European"
        )
        self.country = Country.objects.create(
            name="Italy",
            alpha2_code="IT",
            alpha3_code="ITA",
            demonym="Italian",
            continent=self.continent,
        )
        self.driver = Driver.objects.create(
            first_name="Charles",
            last_name="Leclerc",
            abbreviation="LEC",
            permanent_number=16,
            gender="Male",
            date_of_birth="1997-10-16",
            place_of_birth="Monte Carlo",
            country_of_birth=self.country,
            nationality=self.country,
        )

    def test_driver_creation(self):
        self.assertEqual(self.driver.first_name, "Charles")
        self.assertEqual(
            str(self.driver), "Charles Leclerc"
        )


class DriverStandingModelTest(TestCase):
    def setUp(self):
        # Tworzenie niezbędnych danych
        self.continent = Continent.objects.create(
            code="EU", name="Europe", demonym="European"
        )
        self.country = Country.objects.create(
            name="Italy",
            alpha2_code="IT",
            alpha3_code="ITA",
            demonym="Italian",
            continent=self.continent,
        )
        self.circuit = Circuit.objects.create(
            name="Monza",
            full_name="Autodromo Nazionale Monza",
            circuit_type="Permanent",
            place_name="Monza",
            country=self.country,
            latitude=45.6182,
            longitude=9.2818,
        )
        self.race = Race.objects.create(
            season=2023,
            round=14,
            date="2023-09-03",
            official_name="Italian Grand Prix",
            qualifying_format="Standard",
            circuit=self.circuit,
            course_length=5.793,
            laps=53,
            distance=306.72,
        )

        self.driver = Driver.objects.create(
            first_name="Charles",
            last_name="Leclerc",
            abbreviation="LEC",
            permanent_number=16,
            gender="Male",
            date_of_birth="1997-10-16",
            place_of_birth="Monte Carlo",
            country_of_birth=self.country,
            nationality=self.country,
        )

        self.standing = DriverStanding.objects.create(
            driver=self.driver, race=self.race, position=1, points=25
        )

    def test_driver_standing_creation(self):
        self.assertEqual(self.standing.position, 1)
        self.assertEqual(self.standing.points, 25)
        self.assertEqual(self.standing.driver, self.driver)

class StandingsModelsTest(TestCase):
    def setUp(self):
        self.continent = Continent.objects.create(
            code="EU", name="Europe", demonym="European"
        )
        self.country = Country.objects.create(
            name="Italy", alpha2_code="IT", alpha3_code="ITA", demonym="Italian", continent=self.continent
        )
        self.circuit = Circuit.objects.create(
            name="Monza", full_name="Autodromo Nazionale Monza", circuit_type="Permanent",
            place_name="Monza", country=self.country, latitude=45.6182, longitude=9.2818
        )
        self.race = Race.objects.create(
            season=2023, round=14, date="2023-09-03", official_name="Italian Grand Prix",
            qualifying_format="Standard", circuit=self.circuit, course_length=5.793, laps=53, distance=306.72
        )
        self.driver = Driver.objects.create(
            first_name="Charles", last_name="Leclerc", abbreviation="LEC", permanent_number=16,
            gender="Male", date_of_birth="1997-10-16", place_of_birth="Monte Carlo",
            country_of_birth=self.country, nationality=self.country
        )
        self.constructor = Constructor.objects.create(
            name="Ferrari", full_name="Scuderia Ferrari", country=self.country
        )

    def test_driver_standing(self):
        standing = DriverStanding.objects.create(
            race=self.race, driver=self.driver, position=1, points=25
        )
        self.assertEqual(str(standing), "Italian Grand Prix - 2023 - Charles Leclerc - Standing: 1")
        self.assertEqual(standing.points, 25)

    def test_constructor_standing(self):
        standing = ConstructorStanding.objects.create(
            race=self.race, constructor=self.constructor, position=1, points=44
        )
        self.assertEqual(str(standing), "Italian Grand Prix - 2023 - Scuderia Ferrari (Ferrari) - Standing: 1")
        self.assertEqual(standing.points, 44)

    def test_fastest_lap(self):
        fastest_lap = FastestLap.objects.create(
            race=self.race, driver=self.driver, constructor=self.constructor, lap=53,
            lap_time="1:21.046", gap=None, interval=None
        )
        self.assertEqual(str(fastest_lap), "Italian Grand Prix - 2023 - Charles Leclerc - Lap: 53 - Time: 1:21.046")

    def test_practice_session(self):
        practice = PracticeSession.objects.create(
        race=self.race, session_number=1, driver=self.driver, constructor=self.constructor,
        position=1, gap="0.200", interval="0.100", laps=20, time="1:21.345"
    )
        self.assertEqual(str(practice), "Italian Grand Prix - 2023 - Practice 1 - Charles Leclerc - Position: 1")

    def test_sprint_qualifying_result(self):
        sprint_qualifying = SprintQualifyingResult.objects.create(
            race=self.race, driver=self.driver, constructor=self.constructor,
            position=1, q1_time="1:20.123", q2_time="1:19.456", q3_time="1:18.789"
        )
        self.assertEqual(sprint_qualifying.position, 1)
        self.assertEqual(sprint_qualifying.q3_time, "1:18.789")

    def test_sprint_race_result(self):
        sprint_race = SprintRaceResult.objects.create(
            race=self.race, driver=self.driver, constructor=self.constructor,
            position=1, laps=17, time="25:12.345", points=8, time_penalty=None
        )
        self.assertEqual(sprint_race.position, 1)
        self.assertEqual(sprint_race.points, 8)

    def test_qualifying_result(self):
        qualifying = QualifyingResult.objects.create(
            race=self.race, driver=self.driver, constructor=self.constructor,
            position=1, q1_time="1:20.123", q2_time="1:19.456", q3_time="1:18.789", laps=15
        )
        self.assertEqual(str(qualifying), "Italian Grand Prix - 2023 - Qualifying - Charles Leclerc - Position: 1")

    def test_race_result(self):
        race_result = RaceResult.objects.create(
            race=self.race,
            driver=self.driver,
            constructor=self.constructor,
            position=1,
            points=25,
            laps=53,
            time="1:32:50.123",
            time_penalty=None,
            gap="0.123",
            interval=None,
            reason_retired=None
        )
        self.assertEqual(
            str(race_result),
            "Italian Grand Prix - 2023 - Charles Leclerc - Position: 1"
        )
        self.assertEqual(race_result.points, 25)
        self.assertEqual(race_result.position, 1)
