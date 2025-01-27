from django.contrib import admin
from django.urls import path, include
from novilism import views
from post import views as post_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', post_views.home, name='home'),
    path('story/', include('post.urls')),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', post_views.edit_profile_view, name='profile'),
    path('feedback/', post_views.feedback_view, name='feedback'),
    path('collaborators/', post_views.collaborators_view, name='collaborators'),
    path('search/', post_views.search_posts, name='search_posts'),
    path('about/', views.about, name='about'),
    path('get_notifications/', views.get_notifications, name='get_notifications'),
    path('mark_as_read/<int:id>/', views.mark_as_read, name='mark_as_read'),
    path('fule/', views.fule,name='fule'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)