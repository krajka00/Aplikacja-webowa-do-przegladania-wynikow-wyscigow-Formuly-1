# Generated by Django 5.1.3 on 2024-11-09 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WynikiF1', '0010_driver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='permanent_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
