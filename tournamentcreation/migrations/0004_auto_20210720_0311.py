# Generated by Django 3.1.13 on 2021-07-19 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournamentcreation', '0003_auto_20210714_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='segment',
            name='match_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tournamentcreation.match'),
        ),
        migrations.AlterField(
            model_name='match',
            name='session_id',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='tournamentcreation.session'),
        ),
    ]