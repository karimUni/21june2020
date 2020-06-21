from django.urls import path
from . import views

urlpatterns = [
    path('get/all/students/', views.get_all_students, name='get_all_students'),
    path('genirate/student/report/', views.genirate_student_report, name='genirate_student_report'),
    path('get/all/classes/', views.get_all_classes, name='get_all_classes'),
    path('genirate/class/report/', views.genirate_class_report, name='genirate_class_report'),
]