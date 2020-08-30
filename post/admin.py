from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Админ модель сообщений"""
    list_display = ['author', 'image', 'text', 'created']
