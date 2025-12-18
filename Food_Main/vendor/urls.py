from django.urls import path
from . import views
from accounts import views as accountViews

urlpatterns = [
    path('', accountViews.vendorDashboard, name='vendor'),
    path('profile/', views.profile, name='profile'),
    path('menu_builder/', views.menu_builder, name="menu_builder"),

    # Category
    path('menu_builder/category/<int:pk>/', views.fooditem_by_category , name="fooditem_by_category"),
    path('menu_builder/category/add/', views.add_category , name="add_category"),
    path('menu_builder/category/edit/<int:cat_id>/', views.edit_category , name="edit_category"),
    path('menu_builder/category/delete/<int:cat_id>/', views.delete_category , name="delete_category"),

    # Food items
    path('menu_builder/food/add/', views.add_food , name="add_food"),
    path('menu_builder/food/edit/<int:food_id>/', views.edit_food , name="edit_food"),
    path('menu_builder/food/delete/<int:food_id>/', views.delete_food , name="delete_food"),
]
