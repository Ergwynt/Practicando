from django.urls import path

from . import views

app_name = 'ingredient'


urlpatterns = [
    path('', views.ingredient_list, name='ingredient-list'),
    path('<int:pk>/', views.ingredients_detail, name='ingredient-detail'),
    path('add/', views.ingredients_add, name='add-ingredient'),
]
