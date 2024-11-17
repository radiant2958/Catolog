from django.contrib import admin
from .models import Category, Material


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'category_code')  # Отображаемые поля
    list_filter = ('parent',)  # Фильтр по родительской категории
    search_fields = ('name', 'category_code')  # Поля для поиска
    ordering = ('id',)  # Сортировка по ID


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'material_code', 'cost')  # Отображаемые поля
    list_filter = ('category',)  # Фильтр по категории
    search_fields = ('name', 'material_code')  # Поля для поиска
    ordering = ('id',)  # Сортировка по ID

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'category_code')
    list_filter = ('parent',)
    search_fields = ('name', 'category_code')
    ordering = ('id',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'material_code', 'cost')
    list_filter = ('category',)
    search_fields = ('name', 'material_code')
    ordering = ('id',)
 