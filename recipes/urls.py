from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipes_list, name='recipes-list'),
    path('<int:pk>/', views.recipes_detail, name='recipes-detail'),
    path('add/', views.add_recipes, name='add-recipes'),
    path('<int:pk>/add-factor/', views.add_factor, name='add-factor'),
]
