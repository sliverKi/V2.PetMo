from django.contrib import admin
from .models import Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=("id","categoryType",)
    list_display_link=("id","categoryType",)