import requests

from datetime import datetime, timedelta

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from config import settings
from habits.models import Habit


def send_welcome_message(obj: Habit):
	token = settings.TG_BOT_TOKEN
	chat_id = obj.owner.tg_id
	message = f"Привет, теперь я буду трекать созданную тобой привычку:{obj.action}."
	requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}")


def create_periodic_task(obj: Habit):
	schedule, created = IntervalSchedule.objects.get_or_create(
		every=int(obj.periodicity),
		period=IntervalSchedule.MINUTES,
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
