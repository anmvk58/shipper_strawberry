from django.urls import path
from . import views

urlpatterns = [
    path('make-bill/', views.make_list_bill_for_ship, name='make_bill'),
    path('search-bill/', views.search_bill, name='search_bill'),
    path('confirm-bill/', views.confirm_bill, name='confirm_bill'),
]