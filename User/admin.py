from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import User, HeadMaster , Teacher , ClassRoom , Subject, Student, DigitsSecurity

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'birth_date']

admin.site.register(User, CustomUserAdmin)
admin.site.register(HeadMaster)
admin.site.register(Teacher)
admin.site.register(ClassRoom)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(DigitsSecurity)