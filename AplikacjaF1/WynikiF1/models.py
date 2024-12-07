from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    race = models.ForeignKey('Race', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.race.official_name} - {self.timestamp}"

class Continent(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    demonym = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=100)
    alpha2_code = models.CharField(max_length=2)
    alpha3_code = models.CharField(max_length=3)
    demonym = models.CharField(max_length=100)
    continent = models.ForeignKey(Continent, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Constructor(models.Model):
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.full_name} ({self.name})"

    
class Circuit(models.Model):
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    circuit_type = models.CharField(max_length=50)
    place_name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.full_name} ({self.name})"

class Driver(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=10)
    permanent_number = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_death = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=100)
    country_of_birth = models.ForeignKey(Country, related_name='country_of_birth', on_delete=models.CASCADE)
    nationality = models.ForeignKey(Country, related_name='nationality', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Race(models.Model):
    season = models.IntegerField()
    round = models.IntegerField()
    date = models.DateField()
    official_name = models.CharField(max_length=200)
    qualifying_format = models.CharField(max_length=50)
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    course_length = models.FloatField()
    laps = models.IntegerField()
    distance = models.FloatField()

    def __str__(self):
        return f"{self.official_name} - {self.season}"

class RaceResult(models.Model):
    race = models.ForeignKey('Race', on_delete=models.CASCADE)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    constructor = models.ForeignKey('Constructor', on_delete=models.CASCADE)
    position = models.IntegerField()
    points = models.FloatField()
    laps = models.IntegerField(null=True, blank=True)
    time = models.CharField(max_length=50, null=True, blank=True)
    time_penalty = models.CharField(max_length=50, null=True, blank=True)
    gap = models.CharField(max_length=50, null=True, blank=True)
    interval = models.CharField(max_length=50, null=True, blank=True)
    reason_retired = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.race} - {self.driver} - Position: {self.position}"

class DriverStanding(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    position = models.IntegerField()
    points = models.FloatField()

    def __str__(self):
        return f"{self.race} - {self.driver} - Standing: {self.position}"

class ConstructorStanding(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)
    position = models.IntegerField()
    points = models.FloatField()

    def __str__(self):
        return f"{self.race} - {self.constructor} - Standing: {self.position}"

class FastestLap(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE, null=True, blank=True)
    lap = models.IntegerField()
    lap_time = models.CharField(max_length=20)
    gap = models.CharField(max_length=10, null=True, blank=True)
    interval = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.race} - {self.driver} - Lap: {self.lap} - Time: {self.lap_time}"
    
class PracticeSession(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    session_number = models.IntegerField()
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)
    position = models.IntegerField()
    gap = models.CharField(max_length=20, null=True, blank=True)
    interval = models.CharField(max_length=20, null=True, blank=True)
    laps = models.IntegerField(null=True, blank=True)
    time = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.race} - Practice {self.session_number} - {self.driver} - Position: {self.position}"

class SprintQualifyingResult(models.Model):
    race = models.ForeignKey('Race', on_delete=models.CASCADE)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    constructor = models.ForeignKey('Constructor', on_delete=models.CASCADE)
    position = models.IntegerField()
    q1_time = models.CharField(max_length=20, null=True, blank=True)
    q2_time = models.CharField(max_length=20, null=True, blank=True)
    q3_time = models.CharField(max_length=20, null=True, blank=True)
    gap = models.CharField(max_length=20, null=True, blank=True)
    interval = models.CharField(max_length=20, null=True, blank=True)
    laps = models.IntegerField(null=True, blank=True)

class SprintRaceResult(models.Model):
    race = models.ForeignKey('Race', on_delete=models.CASCADE)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    constructor = models.ForeignKey('Constructor', on_delete=models.CASCADE)
    position = models.IntegerField()
    laps = models.IntegerField(null=True, blank=True)
    time = models.CharField(max_length=20, null=True, blank=True)
    time_penalty = models.CharField(max_length=20, null=True, blank=True)
    gap = models.CharField(max_length=20, null=True, blank=True)
    interval = models.CharField(max_length=20, null=True, blank=True)
    reason_retired = models.CharField(max_length=200, null=True, blank=True)
    points = models.IntegerField()

class QualifyingResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)
    position = models.IntegerField()
    q1_time = models.CharField(max_length=20, null=True, blank=True)
    q2_time= models.CharField(max_length=20, null=True, blank=True)
    q3_time = models.CharField(max_length=20, null=True, blank=True)
    laps = models.IntegerField(null=True, blank=True)
    gap = models.CharField(max_length=20, null=True, blank=True)
    interval = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.race} - Qualifying - {self.driver} - Position: {self.position}"