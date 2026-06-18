from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('', include('articles.urls')),
    # ===== НОВЫЕ МАРШРУТЫ =====
    path('register/', core_views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', core_views.logout_view, name='logout'),
    path('profile/', core_views.profile_view, name='profile'),
    path('toggle-favorite/<int:coffee_id>/', core_views.toggle_favorite, name='toggle_favorite'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)