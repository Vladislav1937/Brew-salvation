from django.contrib import admin
from .models import CoffeeOrigin, CoffeeSort

@admin.register(CoffeeOrigin)
class CoffeeOriginAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)

@admin.register(CoffeeSort)
class CoffeeSortAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'origin', 'processing', 'is_active')
    list_filter = ('origin', 'processing', 'is_active')
    search_fields = ('name', 'tasting_notes')