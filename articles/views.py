from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models  # для Q
from .models import Article, Category, Comment

def article_list(request, category_slug=None):
    """
    Список статей с фильтром по категории, поиском, сортировкой и пагинацией.
    """
    all_articles = Article.objects.filter(is_published=True).order_by('-published_date')
    
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        all_articles = all_articles.filter(category=current_category)
    
    # ПОИСК
    query = request.GET.get('q')
    if query:
        all_articles = all_articles.filter(
            models.Q(title__icontains=query) | models.Q(content__icontains=query)
        )
    
    # СОРТИРОВКА
    sort = request.GET.get('sort')
    if sort == 'popular':
        all_articles = all_articles.order_by('-views', '-published_date')
    elif sort == 'likes':
        all_articles = all_articles.order_by('-total_likes', '-published_date')
    else:
        all_articles = all_articles.order_by('-published_date')  # новизна по умолчанию
    
    # ПАГИНАЦИЯ
    paginator = Paginator(all_articles, 6)
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'articles': page_obj.object_list,
        'categories': categories,
        'current_category': current_category,
        'query': query,
        'sort': sort,
    }
    return render(request, 'articles/article_list.html', context)


def article_detail(request, slug):
    """
    Детальная страница статьи.
    Обрабатывает POST-запросы для добавления комментариев.
    """
    article = get_object_or_404(
        Article.objects.prefetch_related('images', 'comments'),
        slug=slug,
        is_published=True
    )
    
    # Обработка комментариев
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        comment_text = request.POST.get('comment_text')
        
        if author_name and comment_text:
            Comment.objects.create(
                article=article,
                author_name=author_name,
                text=comment_text,
                is_approved=False  # на модерацию
            )
            messages.success(request, 'Спасибо! Ваш комментарий отправлен на модерацию.')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля.')
        
        return redirect('articles:article_detail', slug=article.slug)
    
    # Одобренные комментарии
    comments = article.comments.filter(is_approved=True)
    
    # Информация о лайках (для отображения в шаблоне)
    total_likes = article.likes.count()
    user_liked = False
    if request.user.is_authenticated:
        user_liked = article.likes.filter(id=request.user.id).exists()
    
    context = {
        'article': article,
        'comments': comments,
        'total_likes': total_likes,
        'user_liked': user_liked,
    }
    return render(request, 'articles/article_detail.html', context)


def brewing_calculator(request):
    """Страница калькулятора заваривания."""
    return render(request, 'articles/brewing_calculator.html')


@csrf_exempt  # если используешь AJAX без CSRF-токена, но лучше передавать токен
def like_article(request, slug):
    """
    AJAX-обработчик лайков: добавляет/убирает лайк, возвращает JSON.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Пожалуйста, войдите на сайт'}, status=401)
    
    article = get_object_or_404(Article, slug=slug)
    
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
        liked = False
    else:
        article.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'total_likes': article.likes.count()
    })