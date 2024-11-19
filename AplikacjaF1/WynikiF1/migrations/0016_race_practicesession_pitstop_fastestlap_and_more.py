# Generated by Django 5.1.3 on 2024-11-11 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WynikiF1', '0015_tyremanufacturer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.IntegerField()),
                ('round', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('circuit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.circuit')),
            ],
        ),
        migrations.CreateModel(
            name='PracticeSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_number', models.IntegerField()),
                ('position', models.IntegerField()),
                ('laps', models.IntegerField()),
                ('status', models.CharField(max_length=100)),
                ('constructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.constructor')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.driver')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.race')),
            ],
        ),
        migrations.CreateModel(
            name='PitStop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stop_number', models.IntegerField()),
                ('lap', models.IntegerField()),
                ('duration', models.CharField(max_length=50)),
                ('time_of_day', models.CharField(max_length=50)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.driver')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.race')),
            ],
        ),
        migrations.CreateModel(
            name='FastestLap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lap_time', models.CharField(max_length=50)),
                ('average_speed', models.FloatField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.driver')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.race')),
            ],
        ),
        migrations.CreateModel(
            name='DriverStanding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('points', models.FloatField()),
                ('wins', models.IntegerField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.driver')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.race')),
            ],
        ),
        migrations.CreateModel(
            name='ConstructorStanding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('points', models.FloatField()),
                ('wins', models.IntegerField()),
                ('constructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.constructor')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.race')),
            ],
        ),
        migrations.CreateModel(
            name='RaceResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('points', models.FloatField()),
                ('laps', models.IntegerField()),
                ('status', models.CharField(max_length=100)),
                ('constructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.constructor')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.driver')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.race')),
            ],
        ),
        migrations.CreateModel(
            name='StartingGrid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.driver')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.race')),
            ],
        ),
    ]
