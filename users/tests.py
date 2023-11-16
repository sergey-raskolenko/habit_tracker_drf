from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status

from users.models import User


class UserRegistrationTestCase(APITestCase):
	"""Тест-кейс для регистрации пользователя и просмотра списка пользователей"""
	def setUp(self):
		self.data = {
			"email": "test@test.com",
			"password": "Testtest1!",
			"password2": "Testtest1!"
		}

	def test_create_user(self):
		"""Тест для создания пользователя"""
		response = self.client.post(reverse('users:register_user'), data=self.data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(User.objects.exists())

	def test_user_list(self):
		"""Тест для просмотра списка пользователей"""
		response = self.client.get(reverse('users:list_user'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserTestCase(APITestCase):
	"""Тест-кейс для авторизации и механизмов RUD"""
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create(
			email='test@test.com',
			first_name='Test',
			last_name='Testov',
			tg_id='99999'
		)
		self.user.set_password('Testtest1!')
		self.user.save()

	def test_user_login(self):
		"""Тест авторизации пользователя"""
		data = {
			"email": "test@test.com",
			"password": "Testtest1!"
		}
		response = self.client.post(reverse('users:token_obtain_pair'), data=data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_user_profile_view(self):
		"""Тест для просмотра профиля пользователя"""
		self.client.force_authenticate(user=self.user)
		response = self.client.get(reverse('users:rud_user', args=[self.user.id]))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_update_user(self):
		"""Тест для обновления информации о пользователе"""
		self.client.force_authenticate(user=self.user)
		data = {"last_name": "Test"}
		response = self.client.patch(reverse('users:rud_user', args=[self.user.id]), data=data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_delete_user(self):
		"""Тест для удаления пользователя"""
		self.client.force_authenticate(user=self.user)
		response = self.client.delete(reverse('users:rud_user', args=[self.user.id]))
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
