from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError("The given username must be set")
		user = self.model(email=self.normalize_email(email), **extra_fields)
		user.set_password(password)
		user.save()

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault("is_staff", False)
		extra_fields.setdefault("is_superuser", False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)

		if extra_fields.get("is_staff") is not True:
			raise ValueError("Superuser must have is_staff=True.")
		if extra_fields.get("is_superuser") is not True:
			raise ValueError("Superuser must have is_superuser=True.")

		return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
	"""Модель для описания пользователя"""
	objects = UserManager()

	username = None
	email = models.EmailField(unique=True, verbose_name='почта')
	tg_id = models.CharField(max_length=50, verbose_name='Телеграмм id', **NULLABLE)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = []

	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = 'Пользователи'
		db_table = 'users'
		ordering = ['id']

	def __str__(self):
		return self.email
