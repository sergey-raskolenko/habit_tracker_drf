import requests

from datetime import datetime, timedelta

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from config import settings
from habits.models import Habit


def send_welcome_message(obj: Habit) -> None:
	"""
	Функция для отправки пользователю приветственного письма, при создании новой привычки.
	:param obj: объект модели Habit
	:return: None
	"""
	token = settings.TG_BOT_TOKEN
	chat_id = obj.owner.tg_id
	message = f"Привет, теперь я буду трекать созданную тобой привычку:{obj.action}."
	requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}")


def create_periodic_task(obj: Habit) -> None:
	"""
	Функция для создания периодической задачи с расписанием, согласным с полученной привычкой.
	:param obj: объект модели Habit
	:return: None
	"""
	schedule, created = IntervalSchedule.objects.get_or_create(
		every=int(obj.periodicity),
		period=IntervalSchedule.DAYS,
	)
	if datetime.now().time() < obj.time:
		start_time = datetime.combine(datetime.today(), obj.time)
	else:
		start_time = datetime.combine(datetime.today() + timedelta(days=1), obj.time)

	PeriodicTask.objects.create(
		interval=schedule,
		name=obj,
		task='habits.tasks.send_habit_notification',
		start_time=start_time,
		args=[obj.pk]
	)
