# Generated by Django 5.1.3 on 2024-11-09 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WynikiF1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constructor',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('full_name', models.CharField(max_length=200)),
                ('country_id', models.CharField(max_length=100)),
            ],
        ),
    ]