from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'views', 'likes', 'is_published')
    list_filter = ('is_published', 'uploaded_at')
    search_fields = ('title', 'description')
    readonly_fields = ('views', 'likes', 'uploaded_at', 'updated_at')
    fieldsets = (
        ('معلومات الفيديو', {
            'fields': ('title', 'description', 'file', 'thumbnail')
        }),
        ('الإحصائيات', {
            'fields': ('views', 'likes', 'uploaded_at', 'updated_at')
        }),
        ('الحالة', {
            'fields': ('is_published',)
        }),
    )
