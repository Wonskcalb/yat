from django.urls import path

from . import views


app_name = "todo"

urlpatterns = [
    path('home/', views.home, name='home'),
    path('items/', views.ItemsListView.as_view(), name='items'),
    path('items/<int:id>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('items/<int:id>/toggle/', views.ItemDetailView.toggle_item,
         name='item-detail'),
]