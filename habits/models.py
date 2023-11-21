from django.db import models

from config import settings
from users.models import NULLABLE


class Habit(models.Model):
	"""Модель для описания атомарной привычки"""
	PERIODICITY_CHOICES = (
		(1, 'Раз в 1 день'),
		(2, 'Раз в 2 дня'),
		(3, 'Раз в 3 дня'),
		(4, 'Раз в 4 дня'),
		(5, 'Раз в 5 дней'),
		(6, 'Раз в 6 дней'),
		(7, 'Раз в 7 дней'),
	)

	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)
	place = models.CharField(default='любое место', max_length=100, verbose_name='Место')
	time = models.TimeField(auto_now_add=True, verbose_name='Время')
	action = models.CharField(max_length=100, verbose_name='Действие привычки')
	is_enjoyable = models.BooleanField(default=False, verbose_name='Приятная привычка')
	linked_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Связанная привычка', **NULLABLE)
	periodicity = models.PositiveSmallIntegerField(choices=PERIODICITY_CHOICES, verbose_name='Периодичность')
	reward = models.CharField(max_length=100, verbose_name='Награда', **NULLABLE)
	time_for_action = models.PositiveSmallIntegerField(verbose_name='Время на выполнение')
	is_public = models.BooleanField(default=False, verbose_name='Публичность')

	def __str__(self):
		return self.action

	class Meta:
		verbose_name = 'Привычка'
		verbose_name_plural = 'Привычки'
		db_table = 'habits'
		ordering = ['id']
