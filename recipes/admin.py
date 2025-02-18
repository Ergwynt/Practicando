from django.contrib import admin

from .models import Factor, Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'script')


@admin.register(Factor)
class FactorAdmin(admin.ModelAdmin):
    list_display = ('amount', 'unit')
