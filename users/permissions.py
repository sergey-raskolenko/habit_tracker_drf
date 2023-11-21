from rest_framework.permissions import BasePermission


class IsCurrentUser(BasePermission):
	"""Проверка доступа, является ли текущий пользователь владельцем объекта"""
	def has_permission(self, request, view):
		return request.user == view.get_object()
