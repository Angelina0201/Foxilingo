from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.views import View

from foxilang import functions
from foxilang.forms import RegistrationForm
from foxilang.models import User_Level, Theme, Reward


class GuestView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('main')
        context = {'title': 'Веб-приложение "FOXILINGO"',
                   }
        return render(request, 'guest.html', context=context)


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm
        context = {'title': 'Регистрация нового пользователя',
                   'form': form
                   }
        return render(request, 'registration.html', context=context)

    def post(self, request):
        form = RegistrationForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            form.clean()
            new_user = form.save()
            login(request, new_user)
            User_Level.objects.create(level=0, current_experience=0, border_experience=10, user=new_user)
            for theme in Theme.objects.all():
                Reward.objects.create(exp=theme.access_level + 1, theme_id=theme.id, user=new_user)
            return HttpResponseRedirect('/')
        else:
            context = {'title': 'Регистрация нового пользователя',
                       'form': form,
                       }
            return render(request, 'registration.html', context=context)


class MainView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('guest')
        if request.user.is_superuser:
            return redirect('/admin/')

        context = {'title': 'Главное меню',
                   'user_fullname': get_header_name(request),
                   'experience': User_Level.objects.filter(user=request.user),
                   }
        return render(request, 'themes.html', context=context)


class ThemeView(View):
    def get(self, request, theme_id):
        if not Theme.objects.filter(id=theme_id):
            raise Http404

        for usr in User_Level.objects.filter(user=get_user_id(request)):
            level = int(usr.level)
        for theme in Theme.objects.filter(id=theme_id):
            level_theme = int(theme.access_level)
        context = {'title': 'Теория темы',
                   'user_fullname': get_header_name(request),
                   'experience': User_Level.objects.filter(user=request.user),
                   'theme': Theme.objects.filter(id=theme_id),
                   'theme_id': theme_id,
                   }
        if level < level_theme:
            context.update({'check_level': False})
        else:
            context.update({'check_level': True})
        return render(request, 'theme.html', context=context)


class PracticeView(View):
    def get(self, request, theme_id):
        if not Theme.objects.filter(id=theme_id):
            raise Http404

        for theme in Theme.objects.filter(id=theme_id):
            quest = theme.questions.split(', ')

        context = {'title': 'Практика темы',
                   'user_fullname': get_header_name(request),
                   'experience': User_Level.objects.filter(user=request.user),
                   'theme_id': theme_id,
                   'quest': quest[0],
                   'count_quest': 0,
                   'correct_answer': 0,
                   'exp': 0,
                   'is_practice': True,
                   'theme_id': theme_id,
                   }
        return render(request, 'practice.html', context=context)

    def post(self, request, theme_id):
        for theme in Theme.objects.filter(id=theme_id):
            quest = theme.questions.split(', ')
            len_quest = len(theme.questions.split(', '))
        for theme in Theme.objects.filter(id=theme_id):
            answers = theme.answers.split(', ')
        for reward in Reward.objects.filter(theme_id=theme_id):
            exp_theme = reward.exp

        if request.method == "POST":
            count_quest = int(request.POST.get('count_quest'))
            correct_answer = int(request.POST.get('correct_answer'))
            exp = int(request.POST.get('exp'))
            while True:
                answer_user = request.POST.get('answer_user').strip().lower()
                if answer_user == answers[count_quest]:
                    correct_answer += 1
                    exp = exp + exp_theme
                count_quest += 1
                if len_quest == count_quest:
                    quest = None
                else:
                    quest = quest[count_quest]
                context = {'title': 'Практика темы',
                           'user_fullname': get_header_name(request),
                           'experience': User_Level.objects.filter(user=request.user),
                           'quest': quest,
                           'count_quest': count_quest,
                           'correct_answer': correct_answer,
                           'exp': exp,
                           'is_practice': True,
                           'theme_id': theme_id,
                           }
                if len_quest == count_quest:
                    break
                return render(request, 'practice.html', context=context)
            context = {'title': 'Практика темы',
                       'user_fullname': get_header_name(request),
                       'experience': User_Level.objects.filter(user=request.user),
                       'count_quest': count_quest,
                       'len_questions': len_quest,
                       'correct_answer': correct_answer,
                       'exp': exp,
                       'is_practice': False,
                       'theme_id': theme_id,
                       }
            for usr in User_Level.objects.filter(user=get_user_id(request)):
                current_experience = int(usr.current_experience)
                border_experience = int(usr.border_experience)
                level = int(usr.level)
            new_current_experience = current_experience + exp
            if new_current_experience >= border_experience:
                new_current_experience = new_current_experience - border_experience
                new_border_experience = border_experience + 5
                new_level = level + 1
                context.update({'new_level': True, 'new_level_congratulations': new_level})
            else:
                new_border_experience = border_experience
                new_level = level
            functions.update_user_level(user_id=get_user_id(request),
                                        level=new_level,
                                        current_experience=new_current_experience,
                                        border_experience=new_border_experience)
            return render(request, 'practice.html', context=context)


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ошибка 404, Страница не найдена! Возможно вы зашли в не свои события!')


def custom_handler500(request):
    return HttpResponse("Ошибка 500,либо что-то сломалось, либо вы зашли в не свои события!")


# Вспомогательные функции


def get_user_id(request):
    return User.objects.get(username=request.user.get_username())


def get_header_name(request):
    if request.user.get_full_name():
        return request.user.get_full_name()
    else:
        return request.user.username

