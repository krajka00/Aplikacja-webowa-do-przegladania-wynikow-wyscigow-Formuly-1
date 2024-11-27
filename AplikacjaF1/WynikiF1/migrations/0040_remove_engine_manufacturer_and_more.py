# Generated by Django 5.1.3 on 2024-11-27 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WynikiF1', '0039_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engine',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='enginemanufacturer',
            name='country',
        ),
        migrations.DeleteModel(
            name='Entrant',
        ),
        migrations.RemoveField(
            model_name='sprintstartinggrid',
            name='driver',
        ),
        migrations.RemoveField(
            model_name='sprintstartinggrid',
            name='race',
        ),
        migrations.RemoveField(
            model_name='startinggrid',
            name='driver',
        ),
        migrations.RemoveField(
            model_name='startinggrid',
            name='race',
        ),
        migrations.RemoveField(
            model_name='tyremanufacturer',
            name='country',
        ),
        migrations.DeleteModel(
            name='Engine',
        ),
        migrations.DeleteModel(
            name='EngineManufacturer',
        ),
        migrations.DeleteModel(
            name='SprintStartingGrid',
        ),
        migrations.DeleteModel(
            name='StartingGrid',
        ),
        migrations.DeleteModel(
            name='TyreManufacturer',
        ),
    ]
