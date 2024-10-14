from django.contrib import admin
from tests.models import Test, TestResult, OpenAnswer


# Register your models here.
# admin.site.register(Question)
admin.site.register(OpenAnswer)
admin.site.register(Test)
admin.site.register(TestResult)
