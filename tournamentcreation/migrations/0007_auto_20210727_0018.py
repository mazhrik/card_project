# Generated by Django 3.1.13 on 2021-07-26 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournamentcreation', '0006_auto_20210725_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_number',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
