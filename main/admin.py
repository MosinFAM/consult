from django.contrib import admin
from .models import Course, Lesson, Question, Answer, UserProgress

# Register your models here.
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserProgress)