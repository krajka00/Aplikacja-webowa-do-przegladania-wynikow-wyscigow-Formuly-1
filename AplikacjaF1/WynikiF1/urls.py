from django.urls import path
from .views import(UserRegistrationView, LogoutView, CurrentStandingsView, RaceDetailsView, RaceUpdateView, DriverStandingUpdateView, ConstructorStandingUpdateView,
                    FastestLapUpdateView, FastestLapCreateView, FastestLapDeleteView, PitStopUpdateView, PitStopCreateView, PitStopDeleteView,QualifyingResultUpdateView, QualifyingResultCreateView, 
                    QualifyingResultDeleteView, SprintQualifyingResultUpdateView, SprintQualifyingResultCreateView, SprintQualifyingResultDeleteView, SprintRaceResultUpdateView,
                    SprintRaceResultCreateView, SprintRaceResultDeleteView, PracticeSessionUpdateView, PracticeSessionCreateView, PracticeSessionDeleteView, RaceUpdateView, RaceCreateView,
                    RaceDeleteView, DriverStandingUpdateView, DriverStandingCreateView, DriverStandingDeleteView, ConstructorStandingUpdateView, ConstructorStandingCreateView,
                    ConstructorStandingDeleteView, CommentForRaceView, CommentCreateView, CommentDeleteView, RaceListView, ContinentCreateView, ContinentUpdateView, ContinentDeleteView, ContinentRetrieveView, ContinentListView,
                    CountryCreateView, CountryUpdateView, CountryDeleteView, CountryRetrieveView, CountryListView,
                    ConstructorCreateView, ConstructorUpdateView, ConstructorDeleteView, ConstructorRetrieveView, ConstructorListView,
                    CircuitCreateView, CircuitUpdateView, CircuitDeleteView, CircuitRetrieveView, CircuitListView,
                    DriverCreateView, DriverUpdateView, DriverDeleteView, DriverRetrieveView, DriverListView,
                    DriverStandingRetrieveView, DriverStandingListView, ConstructorStandingRetrieveView, ConstructorStandingListView,
                    RaceRetrieveView, FastestLapRetrieveView, FastestLapListView,
                    PitStopRetrieveView, PitStopListView, QualifyingResultRetrieveView, QualifyingResultListView,
                    SprintQualifyingResultRetrieveView, SprintQualifyingResultListView, SprintRaceResultRetrieveView, SprintRaceResultListView,
                    PracticeSessionRetrieveView, PracticeSessionListView, RaceResultCreateView, RaceResultListView, RaceResultUpdateView, RaceListView2, ConstructorStandingAllView, DriverStandingAllView)
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('standings/current/', CurrentStandingsView.as_view(), name='current_standings'),
    path('races/<int:race_id>/', RaceDetailsView.as_view(), name='race_details'),
    path('races/all/<int:year>/', RaceListView.as_view(), name='race_list'),
    path('races/<int:race_id>/comments/', CommentForRaceView.as_view(), name='race_comments'),
    path('races/<int:race_id>/comments/create/', CommentCreateView.as_view(), name='comment_create'),
    path('races/<int:race_id>/comments/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
    path('fastest_lap/update/<int:pk>/', FastestLapUpdateView.as_view(), name='fastest_lap_update'),
    path('fastest_lap/delete/<int:pk>/', FastestLapDeleteView.as_view(), name='fastest_lap_delete'),
    path('fastest_lap/create/', FastestLapCreateView.as_view(), name='fastest_lap_create'),
    path('fastest_lap/<int:pk>/', FastestLapRetrieveView.as_view(), name='fastest_lap_retrieve'),
    path('fastest_lap/', FastestLapListView.as_view(), name='fastest_lap_list'),
    path('pit_stop/update/<int:pk>/', PitStopUpdateView.as_view(), name='pit_stop_update'),
    path('pit_stop/delete/<int:pk>/', PitStopDeleteView.as_view(), name='pit_stop_delete'),
    path('pit_stop/create/', PitStopCreateView.as_view(), name='pit_stop_create'),
    path('pit_stop/<int:pk>/', PitStopRetrieveView.as_view(), name='pit_stop_retrieve'),
    path('pit_stop/', PitStopListView.as_view(), name='pit_stop_list'),
    path('qualifying_result/update/<int:pk>/', QualifyingResultUpdateView.as_view(), name='qualifying_result_update'),
    path('qualifying_result/delete/<int:pk>/', QualifyingResultDeleteView.as_view(), name='qualifying_result_delete'),
    path('qualifying_result/create/', QualifyingResultCreateView.as_view(), name='qualifying_result_create'),
    path('qualifying_result/<int:pk>/', QualifyingResultRetrieveView.as_view(), name='qualifying_result_retrieve'),
    path('qualifying_result/', QualifyingResultListView.as_view(), name='qualifying_result_list'),
    path('sprint_qualifying_result/update/<int:pk>/', SprintQualifyingResultUpdateView.as_view(), name='sprint_qualifying_result_update'),
    path('sprint_qualifying_result/delete/<int:pk>/', SprintQualifyingResultDeleteView.as_view(), name='sprint_qualifying_result_delete'),
    path('sprint_qualifying_result/create/', SprintQualifyingResultCreateView.as_view(), name='sprint_qualifying_result_create'),
    path('sprint_qualifying_result/<int:pk>/', SprintQualifyingResultRetrieveView.as_view(), name='sprint_qualifying_result_retrieve'),
    path('sprint_qualifying_result/', SprintQualifyingResultListView.as_view(), name='sprint_qualifying_result_list'),
    path('sprint_race_result/update/<int:pk>/', SprintRaceResultUpdateView.as_view(), name='sprint_race_result_update'),
    path('sprint_race_result/delete/<int:pk>/', SprintRaceResultDeleteView.as_view(), name='sprint_race_result_delete'),
    path('sprint_race_result/create/', SprintRaceResultCreateView.as_view(), name='sprint_race_result_create'),
    path('sprint_race_result/<int:pk>/', SprintRaceResultRetrieveView.as_view(), name='sprint_race_result_retrieve'),
    path('sprint_race_result/', SprintRaceResultListView.as_view(), name='sprint_race_result_list'),
    path('practice_session/update/<int:pk>/', PracticeSessionUpdateView.as_view(), name='practice_session_update'),
    path('practice_session/delete/<int:pk>/', PracticeSessionDeleteView.as_view(), name='practice_session_delete'),
    path('practice_session/create/', PracticeSessionCreateView.as_view(), name='practice_session_create'),
    path('practice_session/<int:pk>/', PracticeSessionRetrieveView.as_view(), name='practice_session_retrieve'),
    path('practice_session/', PracticeSessionListView.as_view(), name='practice_session_list'),
    path('race/update/<int:pk>/', RaceUpdateView.as_view(), name='race_update'),
    path('race/delete/<int:pk>/', RaceDeleteView.as_view(), name='race_delete'),
    path('race/create/', RaceCreateView.as_view(), name='race_create'),
    path('race/<int:pk>/', RaceRetrieveView.as_view(), name='race_retrieve'),
    path('race/', RaceListView2.as_view(), name='race_list'),
    path('driver_standing/update/<int:pk>/', DriverStandingUpdateView.as_view(), name='driver_standing_update'),
    path('driver_standing/delete/<int:pk>/', DriverStandingDeleteView.as_view(), name='driver_standing_delete'),
    path('driver_standing/create/', DriverStandingCreateView.as_view(), name='driver_standing_create'),
    path('driver_standing/<int:pk>/', DriverStandingRetrieveView.as_view(), name='driver_standing_retrieve'),
    path('driver_standing/', DriverStandingListView.as_view(), name='driver_standing_list'),
    path('constructor_standing/update/<int:pk>/', ConstructorStandingUpdateView.as_view(), name='constructor_standing_update'),
    path('constructor_standing/delete/<int:pk>/', ConstructorStandingDeleteView.as_view(), name='constructor_standing_delete'),
    path('constructor_standing/create/', ConstructorStandingCreateView.as_view(), name='constructor_standing_create'),
    path('constructor_standing/<int:pk>/', ConstructorStandingRetrieveView.as_view(), name='constructor_standing_retrieve'),
    path('constructor_standing/', ConstructorStandingListView.as_view(), name='constructor_standing_list'),
    path('continent/create/', ContinentCreateView.as_view(), name='continent_create'),
    path('continent/update/<int:pk>/', ContinentUpdateView.as_view(), name='continent_update'),
    path('continent/delete/<int:pk>/', ContinentDeleteView.as_view(), name='continent_delete'),
    path('continent/<int:pk>/', ContinentRetrieveView.as_view(), name='continent_retrieve'),
    path('continent/', ContinentListView.as_view(), name='continent_list'),
    path('country/create/', CountryCreateView.as_view(), name='country_create'),
    path('country/update/<int:pk>/', CountryUpdateView.as_view(), name='country_update'),
    path('country/delete/<int:pk>/', CountryDeleteView.as_view(), name='country_delete'),
    path('country/<int:pk>/', CountryRetrieveView.as_view(), name='country_retrieve'),
    path('country/', CountryListView.as_view(), name='country_list'),
    path('constructor/create/', ConstructorCreateView.as_view(), name='constructor_create'),
    path('constructor/update/<int:pk>/', ConstructorUpdateView.as_view(), name='constructor_update'),
    path('constructor/delete/<int:pk>/', ConstructorDeleteView.as_view(), name='constructor_delete'),
    path('constructor/<int:pk>/', ConstructorRetrieveView.as_view(), name='constructor_retrieve'),
    path('constructor/', ConstructorListView.as_view(), name='constructor_list'),
    path('circuit/create/', CircuitCreateView.as_view(), name='circuit_create'),
    path('circuit/update/<int:pk>/', CircuitUpdateView.as_view(), name='circuit_update'),
    path('circuit/delete/<int:pk>/', CircuitDeleteView.as_view(), name='circuit_delete'),
    path('circuit/<int:pk>/', CircuitRetrieveView.as_view(), name='circuit_retrieve'),
    path('circuit/', CircuitListView.as_view(), name='circuit_list'),
    path('driver/create/', DriverCreateView.as_view(), name='driver_create'),
    path('driver/update/<int:pk>/', DriverUpdateView.as_view(), name='driver_update'),
    path('driver/delete/<int:pk>/', DriverDeleteView.as_view(), name='driver_delete'),
    path('driver/<int:pk>/', DriverRetrieveView.as_view(), name='driver_retrieve'),
    path('driver/', DriverListView.as_view(), name='driver_list'),
    path('race_result/create/', RaceResultCreateView.as_view(), name='race_result_create'),
    path('race_result/update/<int:pk>/', RaceResultUpdateView.as_view(), name='race_result_update'),
    path('race_result/', RaceResultListView.as_view(), name='race_result_list'),
    path('constructor_standing/all/<int:constructor_id>/', ConstructorStandingAllView.as_view(), name='constructor_standing_all'),
    path('driver_standing/all/<int:driver_id>/', DriverStandingAllView.as_view(), name='driver_standing_all'),
]