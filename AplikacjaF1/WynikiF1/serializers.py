from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Comment
from WynikiF1.models import DriverStanding, ConstructorStanding, Race, FastestLap, PitStop, QualifyingResult, SprintQualifyingResult, SprintRaceResult, PracticeSession

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
        return user

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'race', 'user', 'content', 'timestamp']
        read_only_fields = ['user', 'timestamp']

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
