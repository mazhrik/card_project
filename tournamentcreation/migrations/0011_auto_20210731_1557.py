# Generated by Django 3.1.13 on 2021-07-31 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournamentcreation', '0010_auto_20210731_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_number',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
