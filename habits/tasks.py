import requests
from celery import shared_task

from config.settings import TG_BOT_TOKEN
from habits.models import Habit


@shared_task
def send_habit_notification(pk: int):
	obj = Habit.objects.get(pk=pk)
	if obj.linked_habit:
		message = f'Напоминание о привычке!' '\n' f'{obj}' '\n' f'А после {obj.linked_habit.__str__()}'
	else:
		if obj.reward:
			reward = obj.reward
		else:
			reward = "ничего"
		message = f'Напоминание о привычке!' '\n' f'{obj}' '\n' f'И получу {reward}'

	requests.post(f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={obj.owner.tg_id}&text={message}")
