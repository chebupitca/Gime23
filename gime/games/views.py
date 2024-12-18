from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import ProfileEditForm
from .forms import GameUploadForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import ReviewForm
from django.db.models import Q
from .models import Game
from . import models
from .models import Game, Review, Tag
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg
from django.db.models import Count
from django.contrib.auth.models import User
from .models import CustomUser
from django.conf import settings




def index(request):
    tag_filter = request.GET.getlist('tags')  # Получаем выбранные теги из запроса
    games = Game.objects.all()

       # Поиск по названию
    query = request.GET.get('q')
    if query:
        games = games.filter(Q(title__icontains=query))

    if tag_filter:
        # Оставляем только игры, у которых есть все выбранные теги
        games = games.filter(tags__name__in=tag_filter).annotate(
            matched_tags=Count('tags', filter=Q(tags__name__in=tag_filter))
        ).filter(matched_tags=len(tag_filter)).distinct()

    tags = Tag.objects.all()  # Для отображения всех тегов
    return render(request, 'games/index.html', {
        'games': games,
        'tags': tags,
        'tag_filter': tag_filter,
    })


@login_required
def profile(request):
    return render(request, 'games/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'games/edit_profile.html', {'form': form})

@login_required
def user_profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    print(settings.TEMPLATES)
    return render(request, 'games/profile.html', {'user': user})

    


@login_required
def upload_game(request):
    if request.method == 'POST':
        form = GameUploadForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(commit=False)
            game.author = request.user
            game.save()
            form.save_m2m()  # Сохраняем связи с тегами
            return redirect('profile')
    else:
        form = GameUploadForm()
    return render(request, 'games/upload_game.html', {'form': form})

def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    reviews = game.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.game = game
            review.author = request.user
            review.save()
            game.update_average_rating()
            messages.success(request, 'Ваш отзыв добавлен.')
            return redirect('game_detail', game_id=game.id)
    else:
        form = ReviewForm()

    return render(request, 'games/game_detail.html', {
        'game': game,
        'reviews': reviews,
        'average_rating': round(average_rating, 2),
        'form': form,
    })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление на страницу входа после успешной регистрации
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


