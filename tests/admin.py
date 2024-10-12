from django.contrib import admin
from .models import Question, AnswerOption, TestResult, Test

admin.site.register(Question)
admin.site.register(AnswerOption)
admin.site.register(TestResult)
admin.site.register(Test)
