from django.urls import path
from . import views
from accounts import views as accountViews

urlpatterns = [
    path('', accountViews.vendorDashboard, name = 'vendor'),
    path('profile/', views.profile, name = 'profile'),
]
