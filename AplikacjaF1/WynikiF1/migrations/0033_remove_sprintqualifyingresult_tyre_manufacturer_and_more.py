# Generated by Django 5.1.3 on 2024-11-16 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WynikiF1', '0032_rename_q1_qualifyingresult_q1_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sprintqualifyingresult',
            name='tyre_manufacturer',
        ),
        migrations.RemoveField(
            model_name='sprintraceresult',
            name='tyre_manufacturer',
        ),
        migrations.RemoveField(
            model_name='sprintstartinggrid',
            name='tyre_manufacturer',
        ),
        migrations.AlterField(
            model_name='qualifyingresult',
            name='position',
            field=models.IntegerField(),
        ),
    ]