from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("",views.HomePageView.as_view(),name="home"),
     path('profile/update/',views.ProfileUpdateView.as_view(), name='profile_update'),
     path('profile/', views.ProfileSettingsView.as_view(), name='profile_settings'),
]