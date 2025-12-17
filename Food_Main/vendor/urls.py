from django.urls import path
from . import views
from accounts import views as accountViews

urlpatterns = [
    path('', accountViews.vendorDashboard, name='vendor'),
    path('profile/', views.profile, name='profile'),
    path('menu_builder/', views.menu_builder, name="menu_builder"),
    path('menu_builder/category/<int:pk>/', views.fooditem_by_category , name="fooditem_by_category"),
]
