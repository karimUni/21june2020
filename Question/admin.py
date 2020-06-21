from django.contrib import admin
from .models import Question, MCQ, TR, Rate

admin.site.register(Question)
admin.site.register(MCQ)
admin.site.register(TR)
admin.site.register(Rate)
