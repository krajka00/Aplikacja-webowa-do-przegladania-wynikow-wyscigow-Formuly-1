from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import UpdateAPIView, CreateAPIView, DestroyAPIView
from .serializers import UserRegistrationSerializer, CommentSerializer
from .models import Comment
from WynikiF1.models import DriverStanding, ConstructorStanding, Race, FastestLap, PitStop, QualifyingResult, PracticeSession, SprintRaceResult, SprintQualifyingResult, SprintRaceResult, PracticeSession
from WynikiF1.serializers import(DriverStandingSerializer, ConstructorStandingSerializer, RaceSerializer,
                                FastestLapSerializer, PitStopSerializer, QualifyingResultSerializer,
                                SprintQualifyingResultSerializer, SprintRaceResultSerializer, PracticeSessionSerializer
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
        
        # Użytkownik może usunąć tylko swoje komentarze w danym wyścigu
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
                    'position': standing.position,
                    'points': standing.points
                }
                for standing in driver_standings
            ]
            constructor_standings = ConstructorStanding.objects.filter(race=latest_race).order_by('position')
            constructor_data = [
                {
                    'constructor': standing.constructor.name,
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
    permission_classes = []

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

class FastestLapCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = FastestLap.objects.all()
    serializer_class = FastestLapSerializer

class FastestLapUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = FastestLap.objects.all()
    serializer_class = FastestLapSerializer

class FastestLapDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = FastestLap.objects.all()
    serializer_class = FastestLapSerializer

class PitStopCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = PitStop.objects.all()
    serializer_class = PitStopSerializer

class PitStopUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = PitStop.objects.all()
    serializer_class = PitStopSerializer

class PitStopDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = PitStop.objects.all()
    serializer_class = PitStopSerializer

class QualifyingResultCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = QualifyingResult.objects.all()
    serializer_class = QualifyingResultSerializer

class QualifyingResultUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = QualifyingResult.objects.all()
    serializer_class = QualifyingResultSerializer

class QualifyingResultDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = QualifyingResult.objects.all()
    serializer_class = QualifyingResultSerializer

class SprintQualifyingResultCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = SprintQualifyingResult.objects.all()
    serializer_class = SprintQualifyingResultSerializer

class SprintQualifyingResultUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = SprintQualifyingResult.objects.all()
    serializer_class = SprintQualifyingResultSerializer

class SprintQualifyingResultDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = SprintQualifyingResult.objects.all()
    serializer_class = SprintQualifyingResultSerializer

class SprintRaceResultCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = SprintRaceResult.objects.all()
    serializer_class = SprintRaceResultSerializer

class SprintRaceResultUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = SprintRaceResult.objects.all()
    serializer_class = SprintRaceResultSerializer

class SprintRaceResultDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = SprintRaceResult.objects.all()
    serializer_class = SprintRaceResultSerializer

class PracticeSessionCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = PracticeSession.objects.all()
    serializer_class = PracticeSessionSerializer

class PracticeSessionUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = PracticeSession.objects.all()
    serializer_class = PracticeSessionSerializer

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
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = DriverStanding.objects.all()
    serializer_class = DriverStandingSerializer

class DriverStandingUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = DriverStanding.objects.all()
    serializer_class = DriverStandingSerializer

class DriverStandingDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = DriverStanding.objects.all()
    serializer_class = DriverStandingSerializer

class ConstructorStandingCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = ConstructorStanding.objects.all()
    serializer_class = ConstructorStandingSerializer

class ConstructorStandingUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = ConstructorStanding.objects.all()
    serializer_class = ConstructorStandingSerializer

class ConstructorStandingDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = ConstructorStanding.objects.all()
    serializer_class = ConstructorStandingSerializer