# Generated by Django 2.2 on 2020-11-20 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_auto_20201120_1955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='is_sent',
        ),
        migrations.RemoveField(
            model_name='game',
            name='quiz_id_check',
        ),
    ]