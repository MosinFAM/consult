from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from main.models import Course


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Имя")
    last_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Фамилия")

    def __str__(self):
        return f"{self.user.username} Профиль"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


# Создание профиля после создания пользователя
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Сохранение профиля при сохранении пользователя
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# Модель для связи пользователя и курса
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} зарегистрирован на {self.course.title}"
