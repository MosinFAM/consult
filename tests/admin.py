from django.contrib import admin
from tests.models import Question, Answer, FinalTest, Test, TestResult, FinalTestResult, OpenAnswer


# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(FinalTest)
admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(FinalTestResult)
admin.site.register(OpenAnswer)
