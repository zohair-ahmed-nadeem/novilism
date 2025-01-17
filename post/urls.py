from django.contrib import admin
from django.urls import path
from post import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', views.create_post, name='post'),
    path('',views.home, name='home'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)