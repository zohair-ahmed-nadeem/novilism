from django.urls import path, include
from post import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('',views.home, name='post'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/edit/', views.edit_post_view, name='edit_post'),
    path('<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/like/', views.like_post_view, name='like_post'),
    path('<int:post_id>/comment/', views.add_comment_view, name='add_comment'),
    path('<int:post_id>/report/', views.report_post_view, name='report_post'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)