from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.generics import UpdateAPIView, CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth.models import User

from .serializers import UserRegistrationSerializer, CommentSerializer
from .models import (Comment, Continent, Country, Constructor, Chassis, Circuit, Driver,
                    EngineManufacturer, Engine, Entrant, TyreManufacturer, Race, RaceResult,
                    StartingGrid, DriverStanding, ConstructorStanding, FastestLap, PitStop,
                    PracticeSession, SprintQualifyingResult, SprintRaceResult, SprintStartingGrid,
                    QualifyingResult
)
from WynikiF1.models import DriverStanding, ConstructorStanding, Race, FastestLap, PitStop, QualifyingResult, PracticeSession, SprintRaceResult, SprintQualifyingResult, SprintRaceResult, PracticeSession
from WynikiF1.serializers import(DriverStandingSerializer, ConstructorStandingSerializer, RaceSerializer,
                                FastestLapSerializer, PitStopSerializer, QualifyingResultSerializer, SprintQualifyingResultSerializer, SprintRaceResultSerializer, PracticeSessionSerializer,
                                ContinentSerializer, CountrySerializer, ConstructorSerializer, ChassisSerializer, CircuitSerializer, DriverSerializer,
                                EngineManufacturerSerializer, EngineSerializer, EntrantSerializer, TyreManufacturerSerializer, RaceResultSerializer,
)
from django.urls import path

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CustomTokenVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            token = request.data.get('token')
            decoded_token = AccessToken(token)
            user_id = decoded_token['user_id']

            user = User.objects.get(id=user_id)
            return Response({
                'is_superuser': user.is_superuser,
            }, status=status.HTTP_200_OK)

        except Exception:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

class CommentForRaceView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, race_id):
        try:
            race = Race.objects.get(pk=race_id)
            comments = Comment.objects.filter(race=race)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Race.DoesNotExist:
            return Response({'detail': 'Race not found.'}, status=status.HTTP_404_NOT_FOUND)
class CommentCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        user = self.request.user
        if user.groups.filter(name='User').exists() or user.is_staff:
            return super().get_permissions()
        self.permission_denied(self.request, message="Only users with 'User' role can add comments.")

    def perform_create(self, serializer):
        race_id = self.kwargs.get('race_id')
        try:
            race = Race.objects.get(pk=race_id)
        except Race.DoesNotExist:
            raise serializers.ValidationError({"race": ["Race with this ID does not exist."]})

        serializer.save(user=self.request.user, race=race)

class CommentDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.request.user
        race_id = self.kwargs['race_id']
        
        if user.groups.filter(name='Moderator').exists() or user.is_staff:
            return Comment.objects.filter(race_id=race_id)
        
        return Comment.objects.filter(user=user, race_id=race_id)
class CurrentStandingsView(APIView):
    permission_classes = []

    def get(self, request):
        try:
            latest_race = Race.objects.latest('date')
            driver_standings = DriverStanding.objects.filter(race=latest_race).order_by('position')
            driver_data = [
                {
                    'driver': f"{standing.driver.first_name} {standing.driver.last_name}",
                    'driver_id': standing.driver.id,
                    'position': standing.position,
                    'points': standing.points
                }
                for standing in driver_standings
            ]
            constructor_standings = ConstructorStanding.objects.filter(race=latest_race).order_by('position')
            constructor_data = [
                {
                    'constructor': standing.constructor.name,
                    'constructor_id': standing.constructor.id,
                    'position': standing.position,
                    'points': standing.points
                }
                for standing in constructor_standings
            ]

            return Response({
                'latest_race': latest_race.official_name,
                'driver_standings': driver_data,
                'constructor_standings': constructor_data
            }, status=status.HTTP_200_OK)
        except Race.DoesNotExist:
            return Response({'detail': 'No race data available.'}, status=status.HTTP_404_NOT_FOUND)


class RaceDetailsView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def get(self, request, race_id):
        try:
            race = Race.objects.get(pk=race_id)
            
            race_details = {
                'official_name': race.official_name,
                'season': race.season,
                'round': race.round,
                'date': race.date,
                'circuit': race.circuit.full_name,
                'laps': race.laps,
                'distance': race.distance,
                'course_length': race.course_length
            }
            

            race_results = race.raceresult_set.all().order_by('position')
            results_data = [
                {
                    'driver': f"{result.driver.first_name} {result.driver.last_name}",
                    'constructor': result.constructor.name,
                    'position': result.position,
                    'points': result.points,
                    'time': result.time,
                    'laps': result.laps,
                    'gap': result.gap,
                    'interval': result.interval
                }
                for result in race_results
            ]
            
            fastest_laps = FastestLap.objects.filter(race=race).order_by('lap')
            fastest_laps_data = [
                {
                    'driver': f"{lap.driver.first_name} {lap.driver.last_name}",
                    'constructor': lap.constructor.name if lap.constructor else None,
                    'lap': lap.lap,
                    'lap_time': lap.lap_time,
                    'gap': lap.gap,
                    'interval': lap.interval
                }
                for lap in fastest_laps
            ]
            
            pit_stops = PitStop.objects.filter(race=race).order_by('stop_number')
            pit_stops_data = [
                {
                    'driver': f"{stop.driver.first_name} {stop.driver.last_name}",
                    'stop_number': stop.stop_number,
                    'lap': stop.lap,
                    'duration': stop.duration,
                    'time_of_day': stop.time_of_day
                }
                for stop in pit_stops
            ]
            
            qualifying_results = QualifyingResult.objects.filter(race=race).order_by('position')
            qualifying_data = [
                {
                    'driver': f"{result.driver.first_name} {result.driver.last_name}",
                    'constructor': result.constructor.name,
                    'position': result.position,
                    'q1_time': result.q1_time,
                    'q2_time': result.q2_time,
                    'q3_time': result.q3_time,
                    'laps': result.laps,
                    'gap': result.gap,
                    'interval': result.interval
                }
                for result in qualifying_results
            ]

            sprint_qualifying_results = SprintQualifyingResult.objects.filter(race=race).order_by('position')
            sprint_qualifying_data = [
                {
                    'driver': f"{result.driver.first_name} {result.driver.last_name}",
                    'constructor': result.constructor.name,
                    'position': result.position,
                    'q1_time': result.q1_time,
                    'q2_time': result.q2_time,
                    'q3_time': result.q3_time,
                    'gap': result.gap,
                    'interval': result.interval,
                    'laps': result.laps
                }
                for result in sprint_qualifying_results
            ]
            
            sprint_results = SprintRaceResult.objects.filter(race=race).order_by('position')
            sprint_results_data = [
                {
                    'driver': f"{result.driver.first_name} {result.driver.last_name}",
                    'constructor': result.constructor.name,
                    'position': result.position,
                    'laps': result.laps,
                    'time': result.time,
                    'time_penalty': result.time_penalty,
                    'gap': result.gap,
                    'interval': result.interval,
                    'reason_retired': result.reason_retired,
                    'points': result.points
                }
                for result in sprint_results
            ]

            practice_sessions = PracticeSession.objects.filter(race=race).order_by('session_number', 'position')
            practice_sessions_data = [
                {
                    'session_number': session.session_number,
                    'driver': f"{session.driver.first_name} {session.driver.last_name}",
                    'constructor': session.constructor.name,
                    'position': session.position,
                    'laps': session.laps,
                    'time': session.time,
                    'gap': session.gap,
                    'interval': session.interval
                }
                for session in practice_sessions
            ]
            
            return Response({
                'race_details': race_details,
                'results': results_data,
                'fastest_laps': fastest_laps_data,
                'pit_stops': pit_stops_data,
                'qualifying_results': qualifying_data,
                'sprint_qualifying_results': sprint_qualifying_data,
                'sprint_results': sprint_results_data,
                'practice_sessions': practice_sessions_data
            }, status=status.HTTP_200_OK)
        except Race.DoesNotExist:
            return Response({'detail': 'Race not found.'}, status=status.HTTP_404_NOT_FOUND)

class RaceListView(APIView):
    permission_classes = []

    def get(self, request, year):
        races = Race.objects.filter(season=year).order_by('date')
        race_data = [
            {
                'id': race.pk,
                'official_name': race.official_name,
                'season': race.season,
                'round': race.round,
                'date': race.date
            }
            for race in races
        ]
        return Response(race_data, status=status.HTTP_200_OK)

class FastestLapListView(ListAPIView):
    serializer_class = FastestLapSerializer

    def get_queryset(self):
        queryset = FastestLap.objects.all()
        race = self.request.query_params.get('race')
        driver = self.request.query_params.get('driver')
        constructor = self.request.query_params.get('constructor')
        if race:
            queryset = queryset.filter(race_id=race)
        if driver:
            queryset = queryset.filter(driver_id=driver)
        if constructor:
            queryset = queryset.filter(constructor_id=constructor)
        return queryset

class PitStopListView(ListAPIView):
    serializer_class = PitStopSerializer

    def get_queryset(self):
        queryset = PitStop.objects.all()
        race = self.request.query_params.get('race')
        driver = self.request.query_params.get('driver')
        if race:
            queryset = queryset.filter(race_id=race)
        if driver:
            queryset = queryset.filter(driver_id=driver)
        return queryset

class QualifyingResultListView(ListAPIView):
    serializer_class = QualifyingResultSerializer

    def get_queryset(self):
        queryset = QualifyingResult.objects.all()
        race = self.request.query_params.get('race')
        driver = self.request.query_params.get('driver')
        constructor = self.request.query_params.get('constructor')
        if race:
            queryset = queryset.filter(race_id=race)
        if driver:
            queryset = queryset.filter(driver_id=driver)
        if constructor:
            queryset = queryset.filter(constructor_id=constructor)
        return queryset

class SprintQualifyingResultListView(ListAPIView):
    serializer_class = SprintQualifyingResultSerializer

    def get_queryset(self):
        queryset = SprintQualifyingResult.objects.all()
        race = self.request.query_params.get('race')
        driver = self.request.query_params.get('driver')
        constructor = self.request.query_params.get('constructor')
        if race:
            queryset = queryset.filter(race_id=race)
        if driver:
            queryset = queryset.filter(driver_id=driver)
        if constructor:
            queryset = queryset.filter(constructor_id=constructor)
        return queryset

class SprintRaceResultListView(ListAPIView):
    serializer_class = SprintRaceResultSerializer

    def get_queryset(self):
        queryset = SprintRaceResult.objects.all()
        race = self.request.query_params.get('race')
        driver = self.request.query_params.get('driver')
        constructor = self.request.query_params.get('constructor')
        if race:
            queryset = queryset.filter(race_id=race)
        if driver:
            queryset = queryset.filter(driver_id=driver)
        if constructor:
            queryset = queryset.filter(constructor_id=constructor)
        return queryset

class PracticeSessionListView(ListAPIView):
    serializer_class = PracticeSessionSerializer

    def get_queryset(self):
        queryset = PracticeSession.objects.all()
        race = self.request.query_params.get('race')
        driver = self.request.query_params.get('driver')
        constructor = self.request.query_params.get('constructor')
        if race:
            queryset = queryset.filter(race_id=race)
        if driver:
            queryset = queryset.filter(driver_id=driver)
        if constructor:
            queryset = queryset.filter(constructor_id=constructor)
        return queryset

class FastestLapCreateView(CreateAPIView):
    queryset = FastestLap.objects.all()
    serializer_class = FastestLapSerializer

    def perform_create(self, serializer):
        race = self.request.data.get('race')
        driver = self.request.data.get('driver')
        constructor = self.request.data.get('constructor')
        serializer.save(race_id=race, driver_id=driver, constructor_id=constructor)

class FastestLapUpdateView(UpdateAPIView):
    queryset = FastestLap.objects.all()
    serializer_class = FastestLapSerializer

    def perform_update(self, serializer):
        race = self.request.data.get('race')
        driver = self.request.data.get('driver')
        constructor = self.request.data.get('constructor')
        serializer.save(race_id=race, driver_id=driver, constructor_id=constructor)

class FastestLapDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = FastestLap.objects.all()
    serializer_class = FastestLapSerializer

class PitStopCreateView(CreateAPIView):
    queryset = PitStop.objects.all()
    serializer_class = PitStopSerializer

    def perform_create(self, serializer):
        race = self.request.data.get('race')
        driver = self.request.data.get('driver')
        serializer.save(race_id=race, driver_id=driver)

class PitStopUpdateView(UpdateAPIView):
    queryset = PitStop.objects.all()
    serializer_class = PitStopSerializer

    def perform_update(self, serializer):
        race = self.request.data.get('race')
        driver = self.request.data.get('driver')
        serializer.save(race_id=race, driver_id=driver)

class PitStopDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = PitStop.objects.all()
    serializer_class = PitStopSerializer

class QualifyingResultCreateView(CreateAPIView):
    queryset = QualifyingResult.objects.all()
    serializer_class = QualifyingResultSerializer

    def perform_create(self, serializer):
        race = self.request.data.get('race')
        driver = self.request.data.get('driver')
        constructor = self.request.data.get('constructor')
        serializer.save(race_id=race, driver_id=driver, constructor_id=constructor)

class QualifyingResultUpdateView(UpdateAPIView):
    queryset = QualifyingResult.objects.all()
    serializer_class = QualifyingResultSerializer

    def perform_update(self, serializer):
        race = self.request.data.get('race')
        driver = self.request.data.get('driver')
        constructor = self.request.data.get('constructor')
        serializer.save(race_id=race, driver_id=driver, constructor_id=constructor)

class QualifyingResultDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = QualifyingResult.objects.all()
    serializer_class = QualifyingResultSerializer

class SprintQualifyingResultCreateView(CreateAPIView):
    queryset = SprintQualifyingResult.objects.all()
    serializer_class = SprintQualifyingResultSerializer

    def perform_create(self, serializer):
        race = self.request.data.get('race')
        driver = self.request.data.get('driver')
        constructor = self.request.data.get('constructor')
        serializer.save(race_id=race, driver_id=driver, constructor_id=constructor)

class SprintQualifyingResultUpdateView(UpdateAPIView):
    queryset = SprintQualifyingResult.objects.all()
    serializer_class = SprintQualifyingResultSerializer

    def perform_update(self, serializer):
        race = self.request.data.get('race')
        driver = self.request.data.get('driver')
        constructor = self.request.data.get('constructor')
        serializer.save(race_id=race, driver_id=driver, constructor_id=constructor)

class SprintQualifyingResultDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = SprintQualifyingResult.objects.all()
    serializer_class = SprintQualifyingResultSerializer

class SprintRaceResultCreateView(CreateAPIView):
    queryset = SprintRaceResult.objects.all()
    serializer_class = SprintRaceResultSerializer

    def perform_create(self, serializer):
        race = self.request.data.get('race')
        driver = self.request.data.get('driver')
        constructor = self.request.data.get('constructor')
        serializer.save(race_id=race, driver_id=driver, constructor_id=constructor)

class SprintRaceResultUpdateView(UpdateAPIView):
    queryset = SprintRaceResult.objects.all()
    serializer_class = SprintRaceResultSerializer

    def perform_update(self, serializer):
        race = self.request.data.get('race')
        driver = self.request.data.get('driver')
        constructor = self.request.data.get('constructor')
        serializer.save(race_id=race, driver_id=driver, constructor_id=constructor)

class SprintRaceResultDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = SprintRaceResult.objects.all()
    serializer_class = SprintRaceResultSerializer

class PracticeSessionCreateView(CreateAPIView):
    queryset = PracticeSession.objects.all()
    serializer_class = PracticeSessionSerializer

    def perform_create(self, serializer):
        race = self.request.data.get('race')
        driver = self.request.data.get('driver')
        constructor = self.request.data.get('constructor')
        serializer.save(race_id=race, driver_id=driver, constructor_id=constructor)

class PracticeSessionUpdateView(UpdateAPIView):
    queryset = PracticeSession.objects.all()
    serializer_class = PracticeSessionSerializer

    def perform_update(self, serializer):
        race = self.request.data.get('race')
        driver = self.request.data.get('driver')
        constructor = self.request.data.get('constructor')
        serializer.save(race_id=race, driver_id=driver, constructor_id=constructor)

class PracticeSessionDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = PracticeSession.objects.all()
    serializer_class = PracticeSessionSerializer

class RaceCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Race.objects.all()
    serializer_class = RaceSerializer

class RaceUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Race.objects.all()
    serializer_class = RaceSerializer

class RaceDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Race.objects.all()
    serializer_class = RaceSerializer

class DriverStandingCreateView(CreateAPIView):
    queryset = DriverStanding.objects.all()
    serializer_class = DriverStandingSerializer

    def perform_create(self, serializer):
        race = self.request.data.get('race')
        driver = self.request.data.get('driver')
        serializer.save(race_id=race, driver_id=driver)

class DriverStandingUpdateView(UpdateAPIView):
    queryset = DriverStanding.objects.all()
    serializer_class = DriverStandingSerializer

    def perform_update(self, serializer):
        race = self.request.data.get('race')
        driver = self.request.data.get('driver')
        serializer.save(race_id=race, driver_id=driver)

class DriverStandingDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = DriverStanding.objects.all()
    serializer_class = DriverStandingSerializer

class ConstructorStandingCreateView(CreateAPIView):
    queryset = ConstructorStanding.objects.all()
    serializer_class = ConstructorStandingSerializer

    def perform_create(self, serializer):
        race = self.request.data.get('race')
        constructor = self.request.data.get('constructor')
        serializer.save(race_id=race, constructor_id=constructor)

class ConstructorStandingUpdateView(UpdateAPIView):
    queryset = ConstructorStanding.objects.all()
    serializer_class = ConstructorStandingSerializer

    def perform_update(self, serializer):
        race = self.request.data.get('race')
        constructor = self.request.data.get('constructor')
        serializer.save(race_id=race, constructor_id=constructor)

class ConstructorStandingListView(ListAPIView):
    serializer_class = ConstructorStandingSerializer

    def get_queryset(self):
        queryset = ConstructorStanding.objects.all()
        race = self.request.query_params.get('race')
        constructor = self.request.query_params.get('constructor')
        if race:
            queryset = queryset.filter(race_id=race)
        if constructor:
            queryset = queryset.filter(constructor_id=constructor)
        return queryset

class ConstructorStandingDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = ConstructorStanding.objects.all()
    serializer_class = ConstructorStandingSerializer

class ContinentCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer

class ContinentUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer

class ContinentDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer

class ContinentRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer

class ContinentListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Continent.objects.all()
    serializer_class = ContinentSerializer

class CountryCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CountryUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CountryDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CountryRetrieveView(RetrieveAPIView):
    permission_classes = []
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CountryListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class ConstructorCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Constructor.objects.all()
    serializer_class = ConstructorSerializer

class ConstructorUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Constructor.objects.all()
    serializer_class = ConstructorSerializer

class ConstructorDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Constructor.objects.all()
    serializer_class = ConstructorSerializer

class ConstructorRetrieveView(RetrieveAPIView):
    permission_classes = []
    queryset = Constructor.objects.all()
    serializer_class = ConstructorSerializer

class ConstructorListView(ListAPIView):
    permission_classes = []
    queryset = Constructor.objects.all()
    serializer_class = ConstructorSerializer

class ChassisCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Chassis.objects.all()
    serializer_class = ChassisSerializer

class ChassisUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Chassis.objects.all()
    serializer_class = ChassisSerializer

class ChassisDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Chassis.objects.all()
    serializer_class = ChassisSerializer

class ChassisRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Chassis.objects.all()
    serializer_class = ChassisSerializer

class ChassisListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Chassis.objects.all()
    serializer_class = ChassisSerializer

class CircuitCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Circuit.objects.all()
    serializer_class = CircuitSerializer

class CircuitUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Circuit.objects.all()
    serializer_class = CircuitSerializer

class CircuitDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Circuit.objects.all()
    serializer_class = CircuitSerializer

class CircuitRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Circuit.objects.all()
    serializer_class = CircuitSerializer

class CircuitListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Circuit.objects.all()
    serializer_class = CircuitSerializer

class DriverCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class DriverUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class DriverDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class DriverRetrieveView(RetrieveAPIView):
    permission_classes = []
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class DriverListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class EngineManufacturerCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = EngineManufacturer.objects.all()
    serializer_class = EngineManufacturerSerializer

class EngineManufacturerUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = EngineManufacturer.objects.all()
    serializer_class = EngineManufacturerSerializer

class EngineManufacturerDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = EngineManufacturer.objects.all()
    serializer_class = EngineManufacturerSerializer

class EngineManufacturerRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = EngineManufacturer.objects.all()
    serializer_class = EngineManufacturerSerializer

class EngineManufacturerListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = EngineManufacturer.objects.all()
    serializer_class = EngineManufacturerSerializer

class EngineCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Engine.objects.all()
    serializer_class = EngineSerializer

class EngineUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Engine.objects.all()
    serializer_class = EngineSerializer

class EngineDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Engine.objects.all()
    serializer_class = EngineSerializer

class EngineRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Engine.objects.all()
    serializer_class = EngineSerializer

class EngineListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Engine.objects.all()
    serializer_class = EngineSerializer

class EntrantCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Entrant.objects.all()
    serializer_class = EntrantSerializer

class EntrantUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Entrant.objects.all()
    serializer_class = EntrantSerializer

class EntrantDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Entrant.objects.all()
    serializer_class = EntrantSerializer

class EntrantRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Entrant.objects.all()
    serializer_class = EntrantSerializer

class EntrantListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Entrant.objects.all()
    serializer_class = EntrantSerializer

class TyreManufacturerCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = TyreManufacturer.objects.all()
    serializer_class = TyreManufacturerSerializer

class TyreManufacturerUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = TyreManufacturer.objects.all()
    serializer_class = TyreManufacturerSerializer

class TyreManufacturerDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = TyreManufacturer.objects.all()
    serializer_class = TyreManufacturerSerializer

class TyreManufacturerRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TyreManufacturer.objects.all()
    serializer_class = TyreManufacturerSerializer

class TyreManufacturerListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TyreManufacturer.objects.all()
    serializer_class = TyreManufacturerSerializer

class DriverStandingRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DriverStanding.objects.all()
    serializer_class = DriverStandingSerializer

class DriverStandingListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DriverStanding.objects.all()
    serializer_class = DriverStandingSerializer

class DriverStandingListView(ListAPIView):
    serializer_class = DriverStandingSerializer

    def get_queryset(self):
        queryset = DriverStanding.objects.all()
        race = self.request.query_params.get('race')
        driver = self.request.query_params.get('driver')
        if race:
            queryset = queryset.filter(race_id=race)
        if driver:
            queryset = queryset.filter(driver_id=driver)
        return queryset

class ConstructorStandingRetrieveView(RetrieveAPIView):
    permission_classes = []
    queryset = ConstructorStanding.objects.all()
    serializer_class = ConstructorStandingSerializer

class ConstructorStandingListView(ListAPIView):
    permission_classes = []
    queryset = ConstructorStanding.objects.all()
    serializer_class = ConstructorStandingSerializer

class RaceRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Race.objects.all()
    serializer_class = RaceSerializer

class RaceListView2(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Race.objects.all()
    serializer_class = RaceSerializer

class FastestLapRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = FastestLap.objects.all()
    serializer_class = FastestLapSerializer

# class FastestLapListView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = FastestLap.objects.all()
#     serializer_class = FastestLapSerializer

class PitStopRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PitStop.objects.all()
    serializer_class = PitStopSerializer

class PitStopListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PitStop.objects.all()
    serializer_class = PitStopSerializer

class QualifyingResultRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = QualifyingResult.objects.all()
    serializer_class = QualifyingResultSerializer

class QualifyingResultListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = QualifyingResult.objects.all()
    serializer_class = QualifyingResultSerializer

class SprintQualifyingResultRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SprintQualifyingResult.objects.all()
    serializer_class = SprintQualifyingResultSerializer

class SprintQualifyingResultListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SprintQualifyingResult.objects.all()
    serializer_class = SprintQualifyingResultSerializer

class SprintRaceResultRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SprintRaceResult.objects.all()
    serializer_class = SprintRaceResultSerializer

class SprintRaceResultListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SprintRaceResult.objects.all()
    serializer_class = SprintRaceResultSerializer

class PracticeSessionRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PracticeSession.objects.all()
    serializer_class = PracticeSessionSerializer

class PracticeSessionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PracticeSession.objects.all()
    serializer_class = PracticeSessionSerializer

class RaceResultCreateView(CreateAPIView):
    queryset = RaceResult.objects.all()
    serializer_class = RaceResultSerializer

    def perform_create(self, serializer):
        race = self.request.data.get('race')
        driver = self.request.data.get('driver')
        constructor = self.request.data.get('constructor')
        serializer.save(race_id=race, driver_id=driver, constructor_id=constructor)

class RaceResultUpdateView(UpdateAPIView):
    queryset = RaceResult.objects.all()
    serializer_class = RaceResultSerializer

    def perform_update(self, serializer):
        race = self.request.data.get('race')
        driver = self.request.data.get('driver')
        constructor = self.request.data.get('constructor')
        serializer.save(race_id=race, driver_id=driver, constructor_id=constructor)

class RaceResultListView(ListAPIView):
    serializer_class = RaceResultSerializer

    def get_queryset(self):
        queryset = RaceResult.objects.all()
        race = self.request.query_params.get('race')
        driver = self.request.query_params.get('driver')
        constructor = self.request.query_params.get('constructor')
        if race:
            queryset = queryset.filter(race_id=race)
        if driver:
            queryset = queryset.filter(driver_id=driver)
        if constructor:
            queryset = queryset.filter(constructor_id=constructor)
        return queryset

class ConstructorStandingAllView(ListAPIView):
    serializer_class = ConstructorStandingSerializer

    def get_queryset(self):
        constructor_id = self.kwargs.get('constructor_id')
        return ConstructorStanding.objects.filter(constructor_id=constructor_id).order_by('race__date')

class DriverStandingAllView(ListAPIView):
    serializer_class = DriverStandingSerializer

    def get_queryset(self):
        driver_id = self.kwargs.get('driver_id')
        return DriverStanding.objects.filter(driver_id=driver_id).order_by('race__date')