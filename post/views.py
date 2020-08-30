from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Message
from .forms import MessageForm, FilterForm
from .service import user_registr


def user_registration(request):
    """Регистрация пользователя"""
    return user_registr(request)


def message_list(request):
    """Список всех сообщений и добавление нового"""
    messages = Message.objects.all()
    message_form = None

    # фильтрация
    filter_form = FilterForm(request.GET)
    if filter_form.is_valid():
        if filter_form.cleaned_data['ordering']:
            messages = messages.order_by(filter_form.cleaned_data['ordering'])
        if filter_form.cleaned_data['ordering'] == 'perday':
            now = datetime.now() - timedelta(minutes=60 * 24)
            messages = Message.objects.all().filter(created__gte=now)

    # если пользователь аутентифицирован - выводим форму добавления сообщения
    if request.user.is_authenticated:
        if request.method == 'POST':
            message_form = MessageForm(request.POST, request.FILES)
            if message_form.is_valid():
                message_form.save()
                return redirect('message_list')
        else:
            message_form = MessageForm(initial={'author': request.user.pk})

    # пагинация сообщений
    page = request.GET.get('page', 1)
    paginator = Paginator(messages, 10)
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    return render(request, 'message_list.html', {'messages': messages,
                                                 'message_form': message_form, 'filter_form': filter_form})


def message_list_by_user(request, username):
    """Список сообщений конкретного автора"""
    user = User.objects.get(username=username)
    messages = Message.objects.filter(author=user)

    # пагинация
    page = request.GET.get('page', 1)
    paginator = Paginator(messages, 10)
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)
    return render(request, 'message_list_by_user.html', {'messages': messages})


