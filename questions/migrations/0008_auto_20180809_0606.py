# Generated by Django 2.0.7 on 2018-08-09 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0007_auto_20180809_0546'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leaderboard',
            old_name='points',
            new_name='transit_points',
        ),
        migrations.AddField(
            model_name='leaderboard',
            name='trivia_points',
            field=models.IntegerField(default=0),
        ),
    ]