# Generated by Django 5.1.3 on 2024-11-16 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WynikiF1', '0026_remove_raceresult_grid_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raceresult',
            name='laps',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
