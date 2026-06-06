from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="URL-метка")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_filter', args=[self.slug])


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="URL-метка")
    content = models.TextField(verbose_name="Текст статьи")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name="Изображение")
    likes = models.ManyToManyField(User, related_name='liked_articles', blank=True, verbose_name="Лайки")

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['-published_date']

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('articles:article_detail', args=[self.slug])


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images', verbose_name="Статья")
    image = models.ImageField(upload_to='articles/detail/', verbose_name="Изображение")
    caption = models.CharField(max_length=255, blank=True, verbose_name="Подпись")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ['order']
        verbose_name = "Изображение статьи"
        verbose_name_plural = "Изображения статей"

    def __str__(self):
        return f"{self.article.title} - {self.order}"


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField(blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author_name} on {self.article.title}"