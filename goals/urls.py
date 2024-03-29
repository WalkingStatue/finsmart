from django.urls import path
from .views import GoalListView, GoalCreateView, GoalUpdateView, GoalDeleteView, GoalTransactionsAPIView

app_name = 'goals'

urlpatterns = [
    path('', GoalListView.as_view(), name='goal_list'),
    path('create/', GoalCreateView.as_view(), name='goal_create'),
    path('<int:pk>/update/', GoalUpdateView.as_view(), name='goal_update'),
    path('<int:pk>/delete/', GoalDeleteView.as_view(), name='goal_delete'),
    path('api/goals/<int:pk>/transactions/', GoalTransactionsAPIView.as_view(), name='goal-transactions-api'),
]