# Generated by Django 3.1.13 on 2021-08-01 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournamentcreation', '0011_auto_20210731_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='td',
            name='match',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tournamentcreation.match'),
        ),
        migrations.AlterField(
            model_name='td',
            name='bbo_username',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]
