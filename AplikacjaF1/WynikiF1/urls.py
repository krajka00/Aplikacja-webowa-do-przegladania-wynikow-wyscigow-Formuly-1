from django.urls import path
from .views import(UserRegistrationView, LogoutView, CurrentStandingsView, RaceDetailsView, RaceUpdateView, DriverStandingUpdateView, ConstructorStandingUpdateView,
                   FastestLapUpdateView, FastestLapCreateView, FastestLapDeleteView, PitStopUpdateView, PitStopCreateView, PitStopDeleteView,QualifyingResultUpdateView, QualifyingResultCreateView, 
                   QualifyingResultDeleteView, SprintQualifyingResultUpdateView, SprintQualifyingResultCreateView, SprintQualifyingResultDeleteView, SprintRaceResultUpdateView,
                   SprintRaceResultCreateView, SprintRaceResultDeleteView, PracticeSessionUpdateView, PracticeSessionCreateView, PracticeSessionDeleteView, RaceUpdateView, RaceCreateView,
                   RaceDeleteView, DriverStandingUpdateView, DriverStandingCreateView, DriverStandingDeleteView, ConstructorStandingUpdateView, ConstructorStandingCreateView,
                   ConstructorStandingDeleteView, CommentCreateView, CommentDeleteView, RaceListView
)
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('standings/current/', CurrentStandingsView.as_view(), name='current_standings'),
    path('races/<int:race_id>/', RaceDetailsView.as_view(), name='race_details'),
    path('races/all/<int:year>/', RaceListView.as_view(), name='race_list'),

    # FastestLap endpoints

    path('fastest-lap/update/<int:pk>/', FastestLapUpdateView.as_view(), name='fastest_lap_update'),
    path('fastest-lap/create/', FastestLapCreateView.as_view(), name='fastest_lap_create'),
    path('fastest-lap/delete/<int:pk>/', FastestLapDeleteView.as_view(), name='fastest_lap_delete'),

    # URLs for fastest laps
    path('fastest_lap/update/<int:pk>/', FastestLapUpdateView.as_view(), name='fastest_lap_update'),
    path('fastest_lap/delete/<int:pk>/', FastestLapDeleteView.as_view(), name='fastest_lap_delete'),
    path('fastest_lap/create/', FastestLapCreateView.as_view(), name='fastest_lap_create'),

    # URLs for pit stops
    path('pit_stop/update/<int:pk>/', PitStopUpdateView.as_view(), name='pit_stop_update'),
    path('pit_stop/delete/<int:pk>/', PitStopDeleteView.as_view(), name='pit_stop_delete'),
    path('pit_stop/create/', PitStopCreateView.as_view(), name='pit_stop_create'),

    # URLs for qualifying results
    path('qualifying_result/update/<int:pk>/', QualifyingResultUpdateView.as_view(), name='qualifying_result_update'),
    path('qualifying_result/delete/<int:pk>/', QualifyingResultDeleteView.as_view(), name='qualifying_result_delete'),
    path('qualifying_result/create/', QualifyingResultCreateView.as_view(), name='qualifying_result_create'),

    # URLs for sprint qualifying results
    path('sprint_qualifying_result/update/<int:pk>/', SprintQualifyingResultUpdateView.as_view(), name='sprint_qualifying_result_update'),
    path('sprint_qualifying_result/delete/<int:pk>/', SprintQualifyingResultDeleteView.as_view(), name='sprint_qualifying_result_delete'),
    path('sprint_qualifying_result/create/', SprintQualifyingResultCreateView.as_view(), name='sprint_qualifying_result_create'),

    # URLs for sprint race results
    path('sprint_race_result/update/<int:pk>/', SprintRaceResultUpdateView.as_view(), name='sprint_race_result_update'),
    path('sprint_race_result/delete/<int:pk>/', SprintRaceResultDeleteView.as_view(), name='sprint_race_result_delete'),
    path('sprint_race_result/create/', SprintRaceResultCreateView.as_view(), name='sprint_race_result_create'),

    # URLs for practice sessions
    path('practice_session/update/<int:pk>/', PracticeSessionUpdateView.as_view(), name='practice_session_update'),
    path('practice_session/delete/<int:pk>/', PracticeSessionDeleteView.as_view(), name='practice_session_delete'),
    path('practice_session/create/', PracticeSessionCreateView.as_view(), name='practice_session_create'),

    # URLs for races
    path('race/update/<int:pk>/', RaceUpdateView.as_view(), name='race_update'),
    path('race/delete/<int:pk>/', RaceDeleteView.as_view(), name='race_delete'),
    path('race/create/', RaceCreateView.as_view(), name='race_create'),

    # URLs for driver standings
    path('driver_standing/update/<int:pk>/', DriverStandingUpdateView.as_view(), name='driver_standing_update'),
    path('driver_standing/delete/<int:pk>/', DriverStandingDeleteView.as_view(), name='driver_standing_delete'),
    path('driver_standing/create/', DriverStandingCreateView.as_view(), name='driver_standing_create'),

    # URLs for constructor standings
    path('constructor_standing/update/<int:pk>/', ConstructorStandingUpdateView.as_view(), name='constructor_standing_update'),
    path('constructor_standing/delete/<int:pk>/', ConstructorStandingDeleteView.as_view(), name='constructor_standing_delete'),
    path('constructor_standing/create/', ConstructorStandingCreateView.as_view(), name='constructor_standing_create'),
]