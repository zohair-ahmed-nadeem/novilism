from django.contrib import admin
from .models import Feedback, Collaborator, Report

admin.site.register(Feedback)
admin.site.register(Collaborator)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'reason', 'created_at', 'post_owner_email', 'reporter_email')
    search_fields = ('user__username', 'post__title', 'reason', 'post_owner_email', 'reporter_email')

admin.site.register(Report, ReportAdmin)