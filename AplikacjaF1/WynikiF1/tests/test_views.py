from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User, Group
from WynikiF1.models import (
    Continent, Country, Circuit, Driver, Race, Comment, DriverStanding, ConstructorStanding,
    Constructor, FastestLap, QualifyingResult, SprintRaceResult, PracticeSession, RaceResult
)
from rest_framework_simplejwt.tokens import RefreshToken

class RaceAppViewsTestCase(APITestCase):
    def setUp(self):
        # Setting up initial data for testing
        self.client = APIClient()

        # Create groups for permission checks
        self.user_group = Group.objects.create(name='User')
        self.moderator_group = Group.objects.create(name='Moderator')

        # Create a user and assign group
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.user.groups.add(self.user_group)

        # Create another user for admin actions
        self.admin_user = User.objects.create_superuser(username="adminuser", password="adminpassword")

        # Create some basic objects
        self.continent = Continent.objects.create(code="EU", name="Europe", demonym="European")
        self.country = Country.objects.create(name="Italy", alpha2_code="IT", alpha3_code="ITA", demonym="Italian", continent=self.continent)
        self.constructor = Constructor.objects.create(name="Ferrari", full_name="Scuderia Ferrari", country=self.country)
        self.circuit = Circuit.objects.create(name="Monza", full_name="Autodromo Nazionale Monza", circuit_type="Permanent", place_name="Monza", country=self.country, latitude=45.6182, longitude=9.2818)
        self.driver = Driver.objects.create(first_name="Charles", last_name="Leclerc", abbreviation="LEC", permanent_number=16, gender="Male", date_of_birth="1997-10-16", place_of_birth="Monte Carlo", country_of_birth=self.country, nationality=self.country)
        self.race = Race.objects.create(season=2023, round=14, date="2023-09-03", official_name="Italian Grand Prix", qualifying_format="Standard", circuit=self.circuit, course_length=5.793, laps=53, distance=306.72)

    def authenticate_user(self):
        # Authenticate the user using JWT
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def authenticate_admin(self):
        # Authenticate the admin user using JWT
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_user_registration_view(self):
        # Testing User Registration
        data = {"username": "newuser", "email": "newuser@example.com", "password": "newpassword123"}
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "newuser")

    def test_logout_view(self):
        # Testing Logout View
        self.authenticate_user()
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post("/api/logout/", {"refresh": str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_comment_create_view(self):
        # Testing Comment Creation
        self.authenticate_user()
        url = f"/api/races/{self.race.id}/comments/create/"
        data = {"content": "Great race!"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "Great race!")

    def test_comment_delete_view_as_moderator(self):
        # Testing Comment Deletion by Moderator
        self.authenticate_admin()
        comment = Comment.objects.create(race=self.race, user=self.user, content="This is a comment")
        url = f"/api/races/{self.race.id}/comments/delete/{comment.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_current_standings_view(self):
        # Testing Current Standings View
        DriverStanding.objects.create(race=self.race, driver=self.driver, position=1, points=25)
        ConstructorStanding.objects.create(race=self.race, constructor=self.constructor, position=1, points=43)
        response = self.client.get("/api/standings/current/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["latest_race"], "Italian Grand Prix")
        self.assertEqual(len(response.data["driver_standings"]), 1)
        self.assertEqual(len(response.data["constructor_standings"]), 1)

    def test_race_details_view(self):
        # Testing Race Details View
        url = f"/api/races/{self.race.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["race_details"]["official_name"], "Italian Grand Prix")

    def test_race_list_view(self):
        # Testing Race List for a specific year
        response = self.client.get(f"/api/races/all/{self.race.season}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["official_name"], "Italian Grand Prix")

    def test_qualifying_result_create_view(self):
        # Testing Qualifying Result Creation
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        url = f"/api/qualifying_result/create/"
        data = {
            "race": self.race.id,
            "driver": self.driver.id,
            "constructor": self.constructor.id,
            "position": 1,
            "q1_time": "1:20.000",
            "q2_time": "1:19.500",
            "q3_time": "1:18.800",
            "laps": 15
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["position"], 1)

    def test_qualifying_result_update_view(self):
        # Testing Qualifying Result Update
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        qualifying_result = QualifyingResult.objects.create(
            race=self.race,
            driver=self.driver,
            constructor=self.constructor,
            position=2,
            q1_time="1:21.000",
            q2_time="1:20.500",
            q3_time="1:19.800",
            laps=15
        )
        url = f"/api/qualifying_result/update/{qualifying_result.id}/"
        data = {
            "race": self.race.id,
            "driver": self.driver.id,
            "constructor": self.constructor.id,
            "position": 1,
            "q1_time": "1:20.000",
            "q2_time": "1:19.500",
            "q3_time": "1:18.800",
            "laps": 15
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["position"], 1)

    def test_fastest_lap_create_view(self):
        # Testing Fastest Lap Creation
        self.authenticate_user()
        url = f"/api/fastest_lap/create/"
        data = {
            "race": self.race.id,
            "driver": self.driver.id,
            "constructor": self.constructor.id,
            "lap": 53,
            "lap_time": "1:21.046"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["lap"], 53)

    def test_fastest_lap_update_view(self):
        # Testing Fastest Lap Update
        self.authenticate_user()
        fastest_lap = FastestLap.objects.create(
            race=self.race,
            driver=self.driver,
            constructor=self.constructor,
            lap=53,
            lap_time="1:22.000"
        )
        url = f"/api/fastest_lap/update/{fastest_lap.id}/"
        data = {
            "race": self.race.id,
            "driver": self.driver.id,
            "constructor": self.constructor.id,
            "lap": 54,
            "lap_time": "1:21.046"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["lap"], 54)

    def test_constructor_standing_create_view(self):
        # Testing Constructor Standing Creation
        self.authenticate_user()
        url = f"/api/constructor_standing/create/"
        data = {
            "race": self.race.id,
            "constructor": self.constructor.id,
            "position": 1,
            "points": 44
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["position"], 1)

    def test_constructor_standing_update_view(self):
        # Testing Constructor Standing Update
        self.authenticate_user()
        constructor_standing = ConstructorStanding.objects.create(
            race=self.race,
            constructor=self.constructor,
            position=2,
            points=40
        )
        url = f"/api/constructor_standing/update/{constructor_standing.id}/"
        data = {
            "race": self.race.id,
            "constructor": self.constructor.id,
            "position": 1,
            "points": 44
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["position"], 1)

    def test_race_result_create_view(self):
        # Testing Race Result Creation
        self.authenticate_user()
        url = f"/api/race_result/create/"
        data = {
            "race": self.race.id,
            "driver": self.driver.id,
            "constructor": self.constructor.id,
            "position": 1,
            "points": 25,
            "laps": 53,
            "time": "1:32:50.123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["position"], 1)

    def test_race_result_update_view(self):
        # Testing Race Result Update
        self.authenticate_user()
        race_result = RaceResult.objects.create(
            race=self.race,
            driver=self.driver,
            constructor=self.constructor,
            position=2,
            points=18,
            laps=53,
            time="1:33:00.000"
        )
        url = f"/api/race_result/update/{race_result.id}/"
        data = {
            "race": self.race.id,
            "driver": self.driver.id,
            "constructor": self.constructor.id,
            "position": 1,
            "points": 25,
            "laps": 53,
            "time": "1:32:50.123"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["position"], 1)
    
    def test_practice_session_create_view(self):
        # Testing Practice Session Creation
        self.authenticate_user()
        url = f"/api/practice_session/create/"
        data = {
            "race": self.race.id,
            "driver": self.driver.id,
            "constructor": self.constructor.id,
            "session_number": 1,
            "position": 1,
            "laps": 20,
            "time": "1:25.123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["position"], 1)

    def test_practice_session_update_view(self):
        # Testing Practice Session Update
        self.authenticate_user()
        practice_session = PracticeSession.objects.create(
            race=self.race,
            driver=self.driver,
            constructor=self.constructor,
            session_number=1,
            position=2,
            laps=20,
            time="1:26.000"
        )
        url = f"/api/practice_session/update/{practice_session.id}/"
        data = {
            "race": self.race.id,
            "driver": self.driver.id,
            "constructor": self.constructor.id,
            "session_number": 1,
            "position": 1,
            "laps": 20,
            "time": "1:25.123"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["position"], 1)

    def test_sprint_race_result_create_view(self):
        # Testing Sprint Race Result Creation
        self.authenticate_user()
        url = f"/api/sprint_race_result/create/"
        data = {
            "race": self.race.id,
            "driver": self.driver.id,
            "constructor": self.constructor.id,
            "position": 1,
            "points": 8,
            "laps": 17,
            "time": "25:50.123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["position"], 1)

    def test_sprint_race_result_update_view(self):
        # Testing Sprint Race Result Update
        self.authenticate_user()
        sprint_race_result = SprintRaceResult.objects.create(
            race=self.race,
            driver=self.driver,
            constructor=self.constructor,
            position=2,
            points=6,
            laps=17,
            time="26:00.000"
        )
        url = f"/api/sprint_race_result/update/{sprint_race_result.id}/"
        data = {
            "race": self.race.id,
            "driver": self.driver.id,
            "constructor": self.constructor.id,
            "position": 1,
            "points": 8,
            "laps": 17,
            "time": "25:50.123"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["position"], 1)
    
    def tearDown(self):

        self.client.credentials()
