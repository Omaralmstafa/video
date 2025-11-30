"""
روابط تطبيق مشاركة الفيديوهات
"""
from django.urls import path
from . import views

app_name = 'video_share'

urlpatterns = [
    # الصفحة الرئيسية - قائمة الفيديوهات
    path('', views.video_list, name='video_list'),
    
    # مشغل الريلز - عرض جميع الفيديوهات
    path('reels/', views.video_player, name='video_player_all'),
    path('reels/<int:video_id>/', views.video_player, name='video_player'),
    
    # بث الفيديو
    path('stream/<int:video_id>/', views.stream_video, name='stream_video'),
    
    # تفاصيل الفيديو
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),
    
    # إعجاب بالفيديو
    path('api/like/<int:video_id>/', views.like_video, name='like_video'),
    
    # رفع فيديو جديد
    path('upload/', views.upload_video, name='upload_video'),
]
