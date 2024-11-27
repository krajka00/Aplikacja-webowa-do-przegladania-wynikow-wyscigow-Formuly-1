from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Comment
from WynikiF1.models import (DriverStanding, ConstructorStanding, Race, FastestLap, PitStop, QualifyingResult, SprintQualifyingResult, SprintRaceResult, PracticeSession,
 Comment, Continent, Country, Constructor, Chassis, Circuit, Driver, RaceResult)
from django.contrib.auth.models import Group

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()

        user_group = Group.objects.get(name='User')
        user.groups.add(user_group)

        return user

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    race = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'race', 'user', 'content', 'timestamp', 'username']
        read_only_fields = ['user', 'timestamp', 'username', 'race']

class DriverStandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverStanding
        fields = ['id', 'driver', 'race', 'position', 'points']

class ConstructorStandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructorStanding
        fields = ['id', 'constructor', 'race', 'position', 'points']

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['id', 'official_name', 'season', 'round', 'date', 'circuit', 'laps', 'distance', 'course_length']

class FastestLapSerializer(serializers.ModelSerializer):
    class Meta:
        model = FastestLap
        fields = ['id', 'race', 'driver', 'constructor', 'lap', 'lap_time', 'gap', 'interval']

class PitStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = PitStop
        fields = ['id', 'race', 'driver', 'stop_number', 'lap', 'duration', 'time_of_day']

class QualifyingResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualifyingResult
        fields = ['id', 'race', 'driver', 'constructor', 'position', 'q1_time', 'q2_time', 'q3_time', 'laps', 'gap', 'interval']

class SprintQualifyingResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SprintQualifyingResult
        fields = ['id', 'race', 'driver', 'constructor', 'position', 'q1_time', 'q2_time', 'q3_time', 'laps', 'gap', 'interval']

class SprintRaceResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SprintRaceResult
        fields = ['id', 'race', 'driver', 'constructor', 'position', 'laps', 'time', 'time_penalty', 'gap', 'interval', 'reason_retired', 'points']

class PracticeSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeSession
        fields = ['id', 'race', 'session_number', 'driver', 'constructor', 'position', 'laps', 'time', 'gap', 'interval']

class ContinentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Continent
        fields = ['id', 'code', 'name', 'demonym']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'alpha2_code', 'alpha3_code', 'demonym', 'continent']

class ConstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constructor
        fields = ['id', 'name', 'full_name', 'country']

class CircuitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circuit
        fields = ['id', 'name', 'full_name', 'circuit_type', 'place_name', 'country', 'latitude', 'longitude']

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'abbreviation', 'permanent_number', 'gender', 'date_of_birth', 'date_of_death', 'place_of_birth', 'country_of_birth', 'nationality']

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['id', 'season', 'round', 'date', 'official_name', 'qualifying_format', 'circuit', 'course_length', 'laps', 'distance']

class RaceResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceResult
        fields = ['id', 'race', 'driver', 'constructor', 'position', 'points', 'laps', 'time', 'time_penalty', 'gap', 'interval', 'reason_retired']
