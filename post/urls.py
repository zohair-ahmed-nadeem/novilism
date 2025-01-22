from django.contrib import admin
from django.urls import path
from post import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', views.create_post, name='post'),
    path('',views.home, name='home'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/edit/', views.edit_post_view, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)