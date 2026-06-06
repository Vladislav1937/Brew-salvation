from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User  # ДОБАВИТЬ - для лайков

class CoffeeOrigin(models.Model):
    """Страна происхождения кофе"""
    name = models.CharField(max_length=100, verbose_name="Страна")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Страна происхождения"
        verbose_name_plural = "Страны происхождения"

    def __str__(self):
        return self.name


class CoffeeSort(models.Model):
    """Сорт/вид кофе (например, Эфиопия Иргачеффе)"""
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(unique=True)
    origin = models.ForeignKey(CoffeeOrigin, on_delete=models.CASCADE, verbose_name="Происхождение")
    processing = models.CharField(max_length=100, blank=True, verbose_name="Обработка")
    tasting_notes = models.TextField(verbose_name="Вкусовые ноты")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Цена (опционально)")
    image = models.ImageField(upload_to='coffee/', blank=True, null=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Сорт кофе"
        verbose_name_plural = "Сорта кофе"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:coffee_detail', args=[self.slug])