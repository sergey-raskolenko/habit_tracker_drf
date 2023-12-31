# Generated by Django 4.2.4 on 2023-11-13 17:44

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
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(default='любое место', max_length=100, verbose_name='Место')),
                ('time', models.TimeField(auto_now_add=True, verbose_name='Время')),
                ('action', models.CharField(max_length=100, verbose_name='Действие привычки')),
                ('is_enjoyable', models.BooleanField(default=False, verbose_name='Приятная привычка')),
                ('periodicity', models.PositiveSmallIntegerField(choices=[('1', 'Раз в 1 день'), ('2', 'Раз в 2 дня'), ('3', 'Раз в 3 дня'), ('4', 'Раз в 4 дня'), ('5', 'Раз в 5 дней'), ('6', 'Раз в 6 дней'), ('7', 'Раз в 7 дней')], verbose_name='Периодичность')),
                ('reward', models.CharField(blank=True, max_length=100, null=True, verbose_name='Награда')),
                ('time_for_action', models.PositiveSmallIntegerField(verbose_name='Время на выполнение')),
                ('is_public', models.BooleanField(default=False, verbose_name='Публичность')),
                ('linked_habits', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='habits.habit', verbose_name='Связанная привычка')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Привычка',
                'verbose_name_plural': 'Привычки',
                'db_table': 'habits',
            },
        ),
    ]
