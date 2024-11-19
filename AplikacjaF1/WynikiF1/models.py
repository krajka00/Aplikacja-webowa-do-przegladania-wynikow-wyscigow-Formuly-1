from django.db import models

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
    
class Chassis(models.Model):
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    constructor = models.ForeignKey(Constructor, on_delete=models.CASCADE)

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
    full_name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=10)
    permanent_number = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_death = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=100)
    country_of_birth = models.ForeignKey(Country, related_name='country_of_birth', on_delete=models.CASCADE)
    nationality = models.ForeignKey(Country, related_name='nationality', on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

class EngineManufacturer(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Engine(models.Model):
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    manufacturer = models.ForeignKey(EngineManufacturer, on_delete=models.CASCADE)
    capacity = models.FloatField()
    configuration = models.CharField(max_length=50)
    aspiration = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name

class Entrant(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class TyreManufacturer(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Race(models.Model):
    season = models.IntegerField()
    round = models.IntegerField()
    date = models.DateField()
    official_name = models.CharField(max_length=200)
    qualifying_format = models.CharField(max_length=50)
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE)
    circuit_type = models.CharField(max_length=50)
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

class StartingGrid(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    position = models.IntegerField()

    def __str__(self):
        return f"{self.race} - {self.driver} - Grid Position: {self.position}"

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

class PitStop(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    stop_number = models.IntegerField()
    lap = models.IntegerField()
    duration = models.CharField(max_length=50)
    time_of_day = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.race} - {self.driver} - Pit Stop #{self.stop_number}"
    
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

class SprintStartingGrid(models.Model):
    race = models.ForeignKey('Race', on_delete=models.CASCADE)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    position = models.IntegerField()
    grid_penalty = models.CharField(max_length=200, null=True, blank=True)
    time = models.CharField(max_length=20, null=True, blank=True)

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