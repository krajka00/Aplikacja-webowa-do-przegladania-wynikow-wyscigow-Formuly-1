# Generated by Django 5.1.3 on 2024-11-16 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WynikiF1', '0036_remove_sprintstartinggrid_constructor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practicesession',
            name='time',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]