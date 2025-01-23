from django.contrib import admin
from .models import Feedback, Collaborator, Report, Post

admin.site.register(Feedback)
admin.site.register(Collaborator)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'reason', 'created_at', 'post_owner_email', 'reporter_email')
    search_fields = ('user__username', 'post__title', 'reason', 'post_owner_email', 'reporter_email')

admin.site.register(Report, ReportAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'post_date', 'view_count', 'tags')
    search_fields = ('title', 'user__username', 'tags')
    list_filter = ('tags', 'post_date')
    actions = ['delete_selected']

admin.site.register(Post, PostAdmin)