from django import forms
from django.contrib.auth.models import User

from .models import Message


class MessageForm(forms.ModelForm):
    """Форма сообщений"""
    class Meta:
        model = Message
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}


class FilterForm(forms.Form):
    """Форма фильтрации сообщений"""
    ordering = forms.ChoiceField(label="Сортировать", required=False, choices=[
        ["created", "От старого к новому"],
        ["-created", "От нового к старому"],
        ["perday", "За последние 24 часа"]
    ])


class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации пользователя"""
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        """Проверка идентичности паролей"""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['password2']
