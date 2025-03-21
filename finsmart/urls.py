"""
URL configuration for finsmart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls.static import static
from accounts import urls as account_urls
from transactions import urls as transaction_urls
from budgets import urls as budget_urls
from goals import urls as goal_urls
from dashboard import urls as dashboard_urls
from analysis import urls as analysis_urls
from export import urls as export_urls
from import_transactions import urls as import_urls
from django.conf import settings
from .views import LandingPageView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include(account_urls,namespace="account")),
    path("transactions/",include(transaction_urls,namespace="transactions")),
    path("budgets/",include(budget_urls,namespace="budgets")),
    path("goals/",include("goals.urls",namespace="goals")),
    path("",include(dashboard_urls,namespace="dashboard")),
    path("analysis/",include(analysis_urls,namespace="analysis")),
    path("export/",include(export_urls,namespace="export")),
    path("import/",include(import_urls,namespace="import")),
    path('landing/', LandingPageView.as_view(), name='landing_page'),
    path("", include("allauth.urls")),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
