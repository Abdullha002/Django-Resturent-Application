from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.market_place, name='market_place'),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail')
]
