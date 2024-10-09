from django.db import models
from django.contrib.auth.models import User
from main.models import Course


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} Профиль"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


# Модель для связи пользователя и курса
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} зарегистрирован на {self.course.title}"
