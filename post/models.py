from django.db import models

from django.conf import settings


class Message(models.Model):
    """Модель сообщений"""
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users')
    text = models.TextField(verbose_name='Сообщение')
    image = models.ImageField(upload_to='message_image', blank=True, verbose_name='Изображение')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('-created',)

    def __str__(self):
        return self.text
