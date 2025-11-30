from django.db import models
from django.utils import timezone


class Video(models.Model):
    """نموذج الفيديو في قاعدة البيانات"""
    title = models.CharField(
        max_length=200,
        verbose_name='العنوان',
        help_text='عنوان الفيديو'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='الوصف',
        help_text='وصف الفيديو (اختياري)'
    )
    file = models.FileField(
        upload_to='videos/',
        verbose_name='ملف الفيديو'
    )
    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        blank=True,
        null=True,
        verbose_name='صورة مصغرة'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاريخ التحميل'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='تاريخ التحديث'
    )
    views = models.IntegerField(
        default=0,
        verbose_name='عدد المشاهدات'
    )
    likes = models.IntegerField(
        default=0,
        verbose_name='عدد الإعجابات'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='منشور'
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'فيديو'
        verbose_name_plural = 'فيديوهات'

    def __str__(self):
        return self.title

    def get_url(self):
        """الحصول على رابط الفيديو"""
        return self.file.url

    def increment_views(self):
        """زيادة عدد المشاهدات"""
        self.views += 1
        self.save(update_fields=['views'])

    def toggle_like(self):
        """تبديل الإعجاب"""
        self.likes += 1 if self.likes >= 0 else -1
        self.save(update_fields=['likes'])
