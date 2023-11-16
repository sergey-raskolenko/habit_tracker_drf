from django.urls import path

from habits.apps import HabitsConfig
from habits.views import HabitListView, HabitCreateView, PublicHabitListView, HabitReadUpdateDeleteView

app_name = HabitsConfig.name

urlpatterns = [
	path('', HabitListView.as_view(), name='list_habit'),
	path('public/', PublicHabitListView.as_view(), name='public_list_habit'),
	path('create/', HabitCreateView.as_view(), name='create_habit'),
	path('<int:pk>/', HabitReadUpdateDeleteView.as_view(), name='rud_habit'),
]
