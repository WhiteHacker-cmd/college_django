# Generated by Django 2.2 on 2020-11-09 06:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50, null=True)),
                ('question', models.CharField(max_length=200)),
                ('option1', models.CharField(max_length=100)),
                ('option2', models.CharField(max_length=100)),
                ('option3', models.CharField(max_length=100)),
                ('option4', models.CharField(max_length=100)),
                ('answer', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.CharField(max_length=10, unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('score_of_current_user', models.IntegerField(default=0)),
                ('score_of_opponent', models.IntegerField(default=0)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator', to=settings.AUTH_USER_MODEL)),
                ('opponent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='opponent', to=settings.AUTH_USER_MODEL)),
                ('quiz', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quizes', to='quiz.Quiz')),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
