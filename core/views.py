from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from articles.models import Article, Comment
from catalog.models import CoffeeSort

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def profile_view(request):
    # Лайкнутые статьи (через ManyToMany поле likes в Article)
    liked_articles = Article.objects.filter(likes=request.user)
    
    # Комментарии пользователя (по имени, т.к. у вас нет ForeignKey к User)
    user_comments = Comment.objects.filter(author_name=request.user.username)
    
    # Избранные сорта кофе
    favorite_coffees = request.user.favorite_coffees.all()
    
    context = {
        'liked_articles': liked_articles,
        'user_comments': user_comments,
        'favorite_coffees': favorite_coffees,
    }
    return render(request, 'core/profile.html', context)

@login_required
def toggle_favorite(request, coffee_id):
    coffee = get_object_or_404(CoffeeSort, id=coffee_id)
    if coffee.favorites.filter(id=request.user.id).exists():
        coffee.favorites.remove(request.user)
        messages.info(request, f'"{coffee.name}" удалён из избранного.')
    else:
        coffee.favorites.add(request.user)
        messages.success(request, f'"{coffee.name}" добавлен в избранное!')
    return redirect('catalog:coffee_detail', slug=coffee.slug)

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('articles:article_list')