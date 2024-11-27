from django.contrib import admin
from WynikiF1.models import (Race, Circuit, RaceResult,Driver, Constructor, DriverStanding, ConstructorStanding, 
                             FastestLap, PitStop, Continent, Country,SprintQualifyingResult, SprintRaceResult, QualifyingResult)

# Rejestracja wszystkich modeli w admin
admin.site.register(Race)
admin.site.register(Circuit)
admin.site.register(RaceResult)
admin.site.register(Driver)
admin.site.register(Constructor)
admin.site.register(DriverStanding)
admin.site.register(ConstructorStanding)
admin.site.register(FastestLap)
admin.site.register(PitStop)
admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(SprintQualifyingResult)
admin.site.register(SprintRaceResult)
admin.site.register(QualifyingResult)