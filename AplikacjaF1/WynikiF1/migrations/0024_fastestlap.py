# Generated by Django 5.1.3 on 2024-11-16 15:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WynikiF1', '0023_delete_fastestlap'),
    ]

    operations = [
        migrations.CreateModel(
            name='FastestLap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField()),
                ('lap', models.IntegerField()),
                ('lap_time', models.CharField(max_length=20)),
                ('gap', models.CharField(blank=True, max_length=10, null=True)),
                ('interval', models.CharField(blank=True, max_length=10, null=True)),
                ('constructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.constructor')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.driver')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='WynikiF1.race')),
            ],
        ),
    ]