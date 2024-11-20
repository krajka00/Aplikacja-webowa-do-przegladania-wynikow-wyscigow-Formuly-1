from django.urls import path
from .views import(UserRegistrationView, LogoutView, CurrentStandingsView, RaceDetailsView, RaceUpdateView, DriverStandingUpdateView, ConstructorStandingUpdateView,
                   FastestLapUpdateView, FastestLapCreateView, FastestLapDeleteView, PitStopUpdateView, PitStopCreateView, PitStopDeleteView,QualifyingResultUpdateView, QualifyingResultCreateView, 
                   QualifyingResultDeleteView, SprintQualifyingResultUpdateView, SprintQualifyingResultCreateView, SprintQualifyingResultDeleteView, SprintRaceResultUpdateView,
                   SprintRaceResultCreateView, SprintRaceResultDeleteView, PracticeSessionUpdateView, PracticeSessionCreateView, PracticeSessionDeleteView, RaceUpdateView, RaceCreateView,
                   RaceDeleteView, DriverStandingUpdateView, DriverStandingCreateView, DriverStandingDeleteView, ConstructorStandingUpdateView, ConstructorStandingCreateView,
                   ConstructorStandingDeleteView, CommentCreateView, CommentDeleteView
)
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('standings/current/', CurrentStandingsView.as_view(), name='current_standings'),
    path('races/<int:race_id>/', RaceDetailsView.as_view(), name='race_details'),

    # FastestLap endpoints

    path('fastest-lap/update/<int:pk>/', FastestLapUpdateView.as_view(), name='fastest_lap_update'),
    path('fastest-lap/create/', FastestLapCreateView.as_view(), name='fastest_lap_create'),
    path('fastest-lap/delete/<int:pk>/', FastestLapDeleteView.as_view(), name='fastest_lap_delete'),

    # PitStop endpoints
    path('pit-stop/update/<int:pk>/', PitStopUpdateView.as_view(), name='pit_stop_update'),
    path('pit-stop/create/', PitStopCreateView.as_view(), name='pit_stop_create'),
    path('pit-stop/delete/<int:pk>/', PitStopDeleteView.as_view(), name='pit_stop_delete'),

    # QualifyingResult endpoints
    path('qualifying-result/update/<int:pk>/', QualifyingResultUpdateView.as_view(), name='qualifying_result_update'),
    path('qualifying-result/create/', QualifyingResultCreateView.as_view(), name='qualifying_result_create'),
    path('qualifying-result/delete/<int:pk>/', QualifyingResultDeleteView.as_view(), name='qualifying_result_delete'),

    # SprintQualifyingResult endpoints
    path('sprint-qualifying-result/update/<int:pk>/', SprintQualifyingResultUpdateView.as_view(), name='sprint_qualifying_result_update'),
    path('sprint-qualifying-result/create/', SprintQualifyingResultCreateView.as_view(), name='sprint_qualifying_result_create'),
    path('sprint-qualifying-result/delete/<int:pk>/', SprintQualifyingResultDeleteView.as_view(), name='sprint_qualifying_result_delete'),

    # SprintRaceResult endpoints
    path('sprint-race-result/update/<int:pk>/', SprintRaceResultUpdateView.as_view(), name='sprint_race_result_update'),
    path('sprint-race-result/create/', SprintRaceResultCreateView.as_view(), name='sprint_race_result_create'),
    path('sprint-race-result/delete/<int:pk>/', SprintRaceResultDeleteView.as_view(), name='sprint_race_result_delete'),

    # PracticeSession endpoints
    path('practice-session/update/<int:pk>/', PracticeSessionUpdateView.as_view(), name='practice_session_update'),
    path('practice-session/create/', PracticeSessionCreateView.as_view(), name='practice_session_create'),
    path('practice-session/delete/<int:pk>/', PracticeSessionDeleteView.as_view(), name='practice_session_delete'),

    # Race endpoints
    path('race/update/<int:pk>/', RaceUpdateView.as_view(), name='race_update'),
    path('race/create/', RaceCreateView.as_view(), name='race_create'),
    path('race/delete/<int:pk>/', RaceDeleteView.as_view(), name='race_delete'),

    # DriverStanding endpoints
    path('driver-standing/update/<int:pk>/', DriverStandingUpdateView.as_view(), name='driver_standing_update'),
    path('driver-standing/create/', DriverStandingCreateView.as_view(), name='driver_standing_create'),
    path('driver-standing/delete/<int:pk>/', DriverStandingDeleteView.as_view(), name='driver_standing_delete'),

    # ConstructorStanding endpoints
    path('constructor-standing/update/<int:pk>/', ConstructorStandingUpdateView.as_view(), name='constructor_standing_update'),
    path('constructor-standing/create/', ConstructorStandingCreateView.as_view(), name='constructor_standing_create'),
    path('constructor-standing/delete/<int:pk>/', ConstructorStandingDeleteView.as_view(), name='constructor_standing_delete'),

    # Comment endpoints
    path('comment/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
]