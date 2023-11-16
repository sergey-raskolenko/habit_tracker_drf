from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status, serializers

from habits.models import Habit
from users.models import User


class HabitListTestCase(APITestCase):
	"""Тест-кейс для просмотра списков привычек"""
	def setUp(self):
		self.user = User.objects.create(
			email='admin@admin.admin',
			first_name='Admin',
			last_name='Admin',
			is_staff=True,
			is_superuser=True
		)
		self.user.set_password('admin')
		self.user.save()
		self.client.force_authenticate(user=self.user)
		Habit.objects.create(
			action='TestHabit',
			periodicity=1,
			time_for_action=10,
			owner=self.user
		)
		Habit.objects.create(
			action='TestHabit',
			periodicity=1,
			time_for_action=10,
			is_public=True
		)

	def test_public_habit_list(self):
		"""Тест для просмотра списка публичных привычек"""
		response = self.client.get(reverse('habits:public_list_habit'))
		result = response.json().get('results')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertTrue(len(result) == 1)

	def test_own_habits_list(self):
		"""Тест для просмотра списка привычек пользователя"""
		response = self.client.get(reverse('habits:list_habit'))
		result = response.json().get('results')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertTrue(len(result) == 1)


class HabitCreateTestCase(APITestCase):
	"""Тест-кейс создания привычки"""
	def setUp(self):
		self.user = User.objects.create(
			email='admin@admin.admin',
			first_name='Admin',
			last_name='Admin',
			is_staff=True,
			is_superuser=True
		)
		self.user.set_password('admin')
		self.user.save()
		self.client.force_authenticate(user=self.user)
		self.enjoyable_habit = Habit.objects.create(
			action='EnjoyableHabit',
			periodicity=4,
			time_for_action=40,
			is_enjoyable=True,
			owner=self.user
		)
		self.data = {
			"action": "SimpleTestHabit",
			"periodicity": 1,
			"time_for_action": 10
		}

	def test_create_habit(self):
		"""Тест создание простейшей привычки"""
		response = self.client.post(reverse('habits:create_habit'), data=self.data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_habit_with_enjoyable_linked_habit(self):
		"""Тест создания привычки со связанной приятной привычкой"""
		data = {**self.data, "linked_habit": self.enjoyable_habit.pk}
		response = self.client.post(reverse('habits:create_habit'), data=data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_habit_view(self):
		"""Тест детального просмотра информации о привычке"""
		response = self.client.get(reverse('habits:rud_habit', args=[self.enjoyable_habit.pk]))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_habit_validation_error_with_reward_and_linked_habit_error(self):
		"""Тест ошибки создания привычки с наградой и связанной привычкой"""
		data_for_error, data_for_error['is_enjoyable'] = {**self.data, "reward": "1", "linked_habit": 1}, False
		response = self.client.post(reverse('habits:create_habit'), data=data_for_error)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertRaises(serializers.ValidationError)

	def test_create_enjoyable_habit_with_reward_error(self):
		"""Тест ошибки создания приятной привычки с наградой"""
		data = {
			"action": "SimpleTestHabit",
			"is_enjoyable": True,
			"periodicity": 1,
			"reward": "1",
			"time_for_action": 10,
			"is_public": False
		}
		response = self.client.post(reverse('habits:create_habit'), data=data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertRaises(serializers.ValidationError)

	def test_create_enjoyable_habit_with_linked_habit_error(self):
		"""Тест ошибки создания приятной привычки со связанной привычкой"""
		data = {
			"action": "SimpleTestHabit",
			"is_enjoyable": True,
			"periodicity": 1,
			"linked_habit": 1,
			"time_for_action": 10,
			"is_public": False
		}
		response = self.client.post(reverse('habits:create_habit'), data=data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertRaises(serializers.ValidationError)

	def test_create_habit_with_not_enjoyable_linked_habit_error(self):
		"""Тест ошибки создания привычки со связанной не приятной привычкой"""
		not_enjoyable_habit = Habit.objects.create(**self.data)
		data = {**self.data, "linked_habit": not_enjoyable_habit.pk}
		response = self.client.post(reverse('habits:create_habit'), data=data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertRaises(serializers.ValidationError)

	def test_create_habit_periodicity_error(self):
		"""Тест ошибки создания привычки при не верной периодичности"""
		data_for_error, data_for_error['periodicity'] = self.data, 0
		response = self.client.post(reverse('habits:create_habit'), data=data_for_error)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertRaises(serializers.ValidationError)

	def test_create_habit_time_for_action_error(self):
		"""Тест ошибки создания привычки при не верном времени на выполнение"""
		data_for_error, data_for_error['time_for_action'] = self.data, 121
		response = self.client.post(reverse('habits:create_habit'), data=data_for_error)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertRaises(serializers.ValidationError)


class HabitUpdateTestCase(APITestCase):
	"""Тест-кейс обновления привычки"""
	def setUp(self):
		self.user = User.objects.create(
			email='admin@admin.admin',
			first_name='Admin',
			last_name='Admin',
			is_staff=True,
			is_superuser=True
		)
		self.user.set_password('admin')
		self.user.save()
		self.client.force_authenticate(user=self.user)
		self.enjoyable_habit = Habit.objects.create(
			action='EnjoyableHabit',
			periodicity=4,
			time_for_action=40,
			is_enjoyable=True,
			owner=self.user
		)
		self.simple_habit = Habit.objects.create(
			action='SimpleHabit',
			periodicity=4,
			time_for_action=40,
			owner=self.user
		)

	def test_update_habit(self):
		"""Тест простого обновления привычки"""
		data = {'periodicity': 7, 'time_for_action': 120}
		response = self.client.patch(reverse('habits:rud_habit', args=[self.simple_habit.pk]), data=data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_update_habit_periodicity_error(self):
		"""Тест ошибки обновления привычки не верной периодичностью"""
		data_for_error = {"periodicity": 0}
		response = self.client.patch(reverse('habits:rud_habit', args=[self.enjoyable_habit.pk]), data=data_for_error)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertRaises(serializers.ValidationError)

	def test_update_habit_time_for_action_error(self):
		"""Тест ошибки обновления привычки не верным временем на выполнение"""
		data_for_error = {'time_for_action': 121}
		response = self.client.patch(reverse('habits:rud_habit', args=[self.enjoyable_habit.pk]), data=data_for_error)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertRaises(serializers.ValidationError)

	def test_habit_update_enjoyable_habit_with_reward_error(self):
		"""Тест ошибки обновления приятной привычки наградой"""
		data = {
			"reward": "Something"
		}
		response = self.client.patch(reverse('habits:rud_habit', args=[self.enjoyable_habit.pk]), data=data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertRaises(serializers.ValidationError)

	def test_habit_update_enjoyable_habit_with_linked_habit_error(self):
		"""Тест ошибки обновления приятной привычки связанной привычкой"""
		data = {"linked_habit": self.simple_habit.pk}
		response = self.client.patch(reverse('habits:rud_habit', args=[self.enjoyable_habit.pk]), data=data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertRaises(serializers.ValidationError)

	def test_update_habit_with_reward_by_linked_habit_error(self):
		"""Тест ошибки обновления привычки с наградой связанной привычкой"""
		habit_with_reward = Habit.objects.create(
			action='HabitWithReward',
			periodicity=4,
			time_for_action=40,
			reward='1',
			owner=self.user
		)
		data = {"linked_habit": self.enjoyable_habit.pk}
		response = self.client.patch(reverse('habits:rud_habit', args=[habit_with_reward.pk]), data=data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertRaises(serializers.ValidationError)

	def test_update_habit_with_linked_habit_by_reward_error(self):
		"""Тест ошибки обновления привычки со связанной привычкой наградой"""
		habit_with_linked_habit = Habit.objects.create(
			action='HabitWithReward',
			periodicity=4,
			time_for_action=40,
			linked_habit=self.enjoyable_habit,
			owner=self.user
		)
		data = {"reward": "1"}
		response = self.client.patch(reverse('habits:rud_habit', args=[habit_with_linked_habit.pk]), data=data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertRaises(serializers.ValidationError)


class HabitDeleteTestCase(APITestCase):
	"""Тест-кейс удаления привычки"""
	def setUp(self):
		self.user = User.objects.create(
			email='admin@admin.admin',
			first_name='Admin',
			last_name='Admin',
			is_staff=True,
			is_superuser=True
		)
		self.user.set_password('admin')
		self.user.save()
		self.client.force_authenticate(user=self.user)
		self.enjoyable_habit = Habit.objects.create(
			action='EnjoyableHabit',
			periodicity=4,
			time_for_action=40,
			is_enjoyable=True,
			owner=self.user
		)

	def test_delete_habit(self):
		"""Тест на удаление привычки"""
		response = self.client.delete(reverse('habits:rud_habit', args=[self.enjoyable_habit.pk]))
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
