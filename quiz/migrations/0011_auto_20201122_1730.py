# Generated by Django 2.2 on 2020-11-22 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_game_game_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_hash',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
