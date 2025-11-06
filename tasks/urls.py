from django.urls import path
from .views import (
    TaskCreateView,
    TaskListView,
    TaskDetailView,
    DailyProgressListView,
    WeeklyProgressListView
)

urlpatterns = [
    # CRUD
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    # Progress APIs
    path('progress/', DailyProgressListView.as_view(), name='daily-progress'),
    path('progress/weekly/', WeeklyProgressListView.as_view(), name='weekly-progress'),
]
