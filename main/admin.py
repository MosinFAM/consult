from django.contrib import admin
from main.models import Category, Course, Article, Question, Answer, FinalTest, Test, TestResult, FinalTestResult, OpenAnswer


admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Article)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(FinalTest)
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(FinalTestResult)
admin.site.register(OpenAnswer)
