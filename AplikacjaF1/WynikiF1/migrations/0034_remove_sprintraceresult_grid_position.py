# Generated by Django 5.1.3 on 2024-11-16 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WynikiF1', '0033_remove_sprintqualifyingresult_tyre_manufacturer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sprintraceresult',
            name='grid_position',
        ),
    ]
