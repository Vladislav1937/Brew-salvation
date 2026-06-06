from django.contrib import admin
from .models import Category, Article, ArticleImage, Comment


class ArticleImageInline(admin.TabularInline):   # ← определение класса
    model = ArticleImage
    extra = 1
    fields = ('image', 'caption', 'order')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'is_published', 'published_date')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'content')
    date_hierarchy = 'published_date'
    inlines = [ArticleImageInline]               # ← использование класса

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'article', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author_name', 'text']
    list_editable = ['is_approved']
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = '✅ Одобрить выбранные комментарии'
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = '❌ Отклонить выбранные комментарии'