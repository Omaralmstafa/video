# شرح ملف asgi.py

## الموقع
`video_project/asgi.py`

## الوظيفة
ملف إعداد ASGI (Asynchronous Server Gateway Interface). يدعم WebSockets والطلبات غير المتزامنة.

---

## شرح الكود

### 1. الوثائق
```python
"""
ASGI config for video_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
```

---

### 2. الاستيرادات
```python
import os
from django.core.asgi import get_asgi_application
```

**الشرح:**
- `get_asgi_application`: وظيفة Django لإنشاء تطبيق ASGI

---

### 3. إعدادات Django
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_project.settings')
```

---

### 4. تطبيق ASGI
```python
application = get_asgi_application()
```

---

## ما هو ASGI؟

### التعريف
ASGI = Asynchronous Server Gateway Interface

**الوظيفة:**
- معيار Python للطلبات غير المتزامنة
- يدعم HTTP و WebSockets
- أحدث من WSGI

---

## الفرق بين WSGI و ASGI

| الميزة | WSGI | ASGI |
|--------|------|------|
| النوع | متزامن | غير متزامن |
| WebSockets | ❌ | ✅ |
| HTTP | ✅ | ✅ |
| الأداء | جيد | أفضل |
| الاستخدام | شائع | جديد |

---

## متى تستخدم ASGI؟

### استخدم ASGI إذا:
- ✅ تحتاج WebSockets (مثل الدردشة)
- ✅ تطبيقات الوقت الفعلي
- ✅ تريد أداء أفضل

### استخدم WSGI إذا:
- ✅ موقع عادي (HTTP فقط)
- ✅ لا تحتاج WebSockets
- ✅ تريد استقرار أكبر

---

## كيفية الاستخدام

### 1. مع Uvicorn
```bash
uvicorn video_project.asgi:application --host 0.0.0.0 --port 8000
```

**الشرح:**
- `uvicorn`: خادم ASGI
- `video_project.asgi`: المسار للملف
- `application`: المتغير

---

### 2. مع Daphne
```bash
daphne -b 0.0.0.0 -p 8000 video_project.asgi:application
```

---

### 3. في الإنتاج
```bash
# في Procfile
web: uvicorn video_project.asgi:application --host 0.0.0.0 --port $PORT
```

---

## حالياً في المشروع

### الوضع الحالي
```python
application = get_asgi_application()
```

**الشرح:**
- حالياً يعمل كـ WSGI عادي
- لا يستخدم ميزات ASGI المتقدمة
- يمكن ترقيته لاحقاً

---

## ترقية لاستخدام WebSockets (مستقبلاً)

### مثال محتمل
```python
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import video_share.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            video_share.routing.websocket_urlpatterns
        )
    ),
})
```

**الوظيفة:**
- يدعم HTTP و WebSockets
- يتطلب Django Channels

---

## ملاحظات مهمة

1. **حالياً بسيط**: لا يستخدم ميزات متقدمة
2. **مستقبلاً**: يمكن إضافة WebSockets
3. **الاستقرار**: WSGI أكثر استقراراً حالياً
4. **الأداء**: ASGI أسرع للطلبات المتعددة

---

## الخلاصة

هذا الملف:
- ✅ مشابه لـ wsgi.py
- ✅ جاهز للترقية المستقبلية
- ✅ لا يحتاج تعديل حالياً
- ✅ يدعم WebSockets (عند الترقية)

---

## نصيحة

**للإنتاج الحالي:**
- استخدم WSGI (Gunicorn) - أكثر استقراراً
- ASGI (Uvicorn) - إذا احتجت WebSockets

**للمستقبل:**
- يمكن ترقية المشروع لاستخدام WebSockets
- مثل: تعليقات مباشرة، إشعارات فورية

