from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('notifications/', views.send_message, name='send_message'),
    path('send_feedback/', views.send_feedback, name='send_feedback'),
    path('list_students/', views.list_students, name='list_students'),
    path('list_teachers/', views.list_teachers, name='list_teachers'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
