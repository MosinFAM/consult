from django.db import models
from django.contrib.auth.models import User


# Категория курса
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name 

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# Курс
class Course(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


# Статья
class Article(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f"Article: {self.title} in {self.course.title}"

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


# # Модель для связи  теста и курса
# class Enrollment(models.Model):
#     article = models.ForeignKey(Article, on_delete=models.CASCADE)
#     test = models.ForeignKey(Test, on_delete=models.CASCADE)
#     enrolled_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} зарегистрирован на {self.course.title}"

# class Test(models.Model):
#     article = models.OneToOneField(Article, on_delete=models.CASCADE)
#     title = models.TextField()

#     def __str__(self):
#         return self.title 
    
#     class Meta:
#         verbose_name = 'Тест'
#         verbose_name_plural = 'Тесты'
# '''
# class Question(models.Model):
#     test = models.ForeignKey(Test, on_delete=models.CASCADE)
#     text = models.TextField()
#     question_type = models.CharField(max_length=50, choices=[('multiple_choice', 'Выбор варианта'), ('text', 'Открытый ответ')])
#     correct_answer = models.TextField(null=True, blank=True)
                                      
#     def __str__(self):
#         return f"Question: {self.text} in {self.test.title}"

#     class Meta:
#         verbose_name = 'Вопрос'
#         verbose_name_plural = 'Вопросы'
    
# class Answer(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     text = models.CharField(max_length=200)
#     is_correct = models.BooleanField(default=False)

#     def __str__(self):
#         return self.text
    
#     class Meta:
#         verbose_name = 'Ответ'
#         verbose_name_plural = 'Ответы'
# '''