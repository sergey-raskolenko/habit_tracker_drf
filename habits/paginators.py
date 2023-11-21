from rest_framework import pagination


class HabitPaginator(pagination.PageNumberPagination):
	"""Пагинация с выводом по 5 объектов на страницу, при максимально возможных - 10"""
	page_size = 5
	page_size_query_param = 'page_size'
	max_page_size = 10
