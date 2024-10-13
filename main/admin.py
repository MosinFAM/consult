from django.contrib import admin
from main.models import Category, Course, Article
from tests.models import Question, Answer


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Article)
admin.site.register(Question)
admin.site.register(Answer)
