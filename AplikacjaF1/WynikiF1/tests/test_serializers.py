from django.test import TestCase
from django.contrib.auth.models import User, Group
from WynikiF1.models import (
    Comment, Continent, Country, Circuit, Driver, Race, DriverStanding, ConstructorStanding,
    FastestLap, QualifyingResult, SprintQualifyingResult, SprintRaceResult, PracticeSession, Constructor, RaceResult
)
from WynikiF1.serializers import (
    UserRegistrationSerializer, CommentSerializer, DriverStandingSerializer, ConstructorStandingSerializer,
    RaceSerializer, FastestLapSerializer, QualifyingResultSerializer, SprintQualifyingResultSerializer,
    SprintRaceResultSerializer, PracticeSessionSerializer, ContinentSerializer, CountrySerializer,
    ConstructorSerializer, CircuitSerializer, DriverSerializer, RaceResultSerializer
)


class SerializerTests(TestCase):
    def setUp(self):
        # Create basic data for testing
        self.continent = Continent.objects.create(code="EU", name="Europe", demonym="European")
        self.country = Country.objects.create(
            name="Italy", alpha2_code="IT", alpha3_code="ITA", demonym="Italian", continent=self.continent
        )
        self.constructor = Constructor.objects.create(name="Ferrari", full_name="Scuderia Ferrari", country=self.country)
        self.circuit = Circuit.objects.create(
            name="Monza", full_name="Autodromo Nazionale Monza", circuit_type="Permanent",
            place_name="Monza", country=self.country, latitude=45.6182, longitude=9.2818
        )
        self.driver = Driver.objects.create(
            first_name="Charles", last_name="Leclerc", abbreviation="LEC", permanent_number=16,
            gender="Male", date_of_birth="1997-10-16", place_of_birth="Monte Carlo",
            country_of_birth=self.country, nationality=self.country
        )
        self.race = Race.objects.create(
            season=2023, round=14, date="2023-09-03", official_name="Italian Grand Prix",
            qualifying_format="Standard", circuit=self.circuit, course_length=5.793, laps=53, distance=306.72
        )

    def test_user_registration_serializer(self):
        data = {"username": "testuser", "email": "testuser@example.com", "password": "securepassword"}
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_comment_serializer(self):
        user = User.objects.create_user(username="testuser", password="password")
        comment = Comment.objects.create(
            race=self.race, user=user, content="Great race!", timestamp="2023-09-03T15:00:00Z"
        )
        serializer = CommentSerializer(comment)
        self.assertEqual(serializer.data["content"], "Great race!")

    def test_driver_standing_serializer(self):
        driver_standing = DriverStanding.objects.create(race=self.race, driver=self.driver, position=1, points=25)
        serializer = DriverStandingSerializer(driver_standing)
        self.assertEqual(serializer.data["points"], 25)

    def test_constructor_standing_serializer(self):
        constructor_standing = ConstructorStanding.objects.create(
            race=self.race, constructor=self.constructor, position=1, points=43
        )
        serializer = ConstructorStandingSerializer(constructor_standing)
        self.assertEqual(serializer.data["points"], 43)

    def test_race_serializer(self):
        serializer = RaceSerializer(self.race)
        self.assertEqual(serializer.data["official_name"], "Italian Grand Prix")

    def test_fastest_lap_serializer(self):
        fastest_lap = FastestLap.objects.create(
            race=self.race, driver=self.driver, constructor=self.constructor, lap=53, lap_time="1:21.046"
        )
        serializer = FastestLapSerializer(fastest_lap)
        self.assertEqual(serializer.data["lap_time"], "1:21.046")

    def test_qualifying_result_serializer(self):
        qualifying = QualifyingResult.objects.create(
            race=self.race, driver=self.driver, constructor=self.constructor, position=1, q1_time="1:22.000"
        )
        serializer = QualifyingResultSerializer(qualifying)
        self.assertEqual(serializer.data["q1_time"], "1:22.000")

    def test_country_serializer(self):
        serializer = CountrySerializer(self.country)
        self.assertEqual(serializer.data["name"], "Italy")

    def test_circuit_serializer(self):
        serializer = CircuitSerializer(self.circuit)
        self.assertEqual(serializer.data["name"], "Monza")
    
    def test_sprint_race_result_serializer(self):
        sprint_race_result = SprintRaceResult.objects.create(
            race=self.race,
            driver=self.driver,
            constructor=self.constructor,
            position=1,
            laps=53,
            time="1:30:00",
            time_penalty="5s",
            gap="10s",
            interval="5s",
            reason_retired=None,
            points=8
        )
        serializer = SprintRaceResultSerializer(sprint_race_result)
        self.assertEqual(serializer.data["points"], 8)
        self.assertEqual(serializer.data["time"], "1:30:00")

    def test_practice_session_serializer(self):
        practice_session = PracticeSession.objects.create(
            race=self.race,
            session_number=1,
            driver=self.driver,
            constructor=self.constructor,
            position=1,
            laps=20,
            time="1:25.000",
            gap="0.5s",
            interval="0.3s"
        )
        serializer = PracticeSessionSerializer(practice_session)
        self.assertEqual(serializer.data["laps"], 20)
        self.assertEqual(serializer.data["time"], "1:25.000")

    def test_continent_serializer(self):
        serializer = ContinentSerializer(self.continent)
        self.assertEqual(serializer.data["name"], "Europe")
        self.assertEqual(serializer.data["code"], "EU")

    def test_sprint_qualifying_result_serializer(self):
        sprint_qualifying = SprintQualifyingResult.objects.create(
            race=self.race,
            driver=self.driver,
            constructor=self.constructor,
            position=1,
            q1_time="1:21.000",
            q2_time="1:20.500",
            q3_time="1:20.000",
            laps=20,
            gap="0.2s",
            interval="0.1s"
        )
        serializer = SprintQualifyingResultSerializer(sprint_qualifying)
        self.assertEqual(serializer.data["q1_time"], "1:21.000")
        self.assertEqual(serializer.data["position"], 1)

    def test_constructor_serializer(self):
        serializer = ConstructorSerializer(self.constructor)
        self.assertEqual(serializer.data["name"], "Ferrari")
        self.assertEqual(serializer.data["full_name"], "Scuderia Ferrari")

    def test_driver_serializer(self):
        serializer = DriverSerializer(self.driver)
        self.assertEqual(serializer.data["first_name"], "Charles")
        self.assertEqual(serializer.data["last_name"], "Leclerc")

    def test_race_result_serializer(self):
        race_result = RaceResult.objects.create(
            race=self.race,
            driver=self.driver,
            constructor=self.constructor,
            position=1,
            points=25,
            laps=53,
            time="1:30:00",
            time_penalty=None,
            gap=None,
            interval=None,
            reason_retired=None
        )
        serializer = RaceResultSerializer(race_result)
        self.assertEqual(serializer.data["position"], 1)
        self.assertEqual(serializer.data["points"], 25)

