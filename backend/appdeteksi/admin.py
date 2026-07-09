from django.contrib import admin
from .models import DetectionHistory, DatasetSample, Profile


@admin.register(DetectionHistory)
class DetectionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'result', 'confidence', 'created_at')
    list_filter = ('result',)
    search_fields = ('user__username', 'result')


@admin.register(DatasetSample)
class DatasetSampleAdmin(admin.ModelAdmin):
    list_display = ('label', 'created_at')
    list_filter = ('label',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
