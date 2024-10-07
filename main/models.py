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


# Тест для статьи
class Test(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=255)

    def __str__(self):
        return f'Test for {self.article.title}'
    
    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


# Вопрос
class Question(models.Model):
    OPEN = 'open'
    CHOICE = 'choice'

    QUESTION_TYPES = [
        (OPEN, 'Open-ended'),
        (CHOICE, 'Multiple choice'),
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default=CHOICE)  # Тип вопроса

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


# Вариант ответа
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, limit_choices_to={'question_type': 'choice'})
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


# Открытые ответы пользователя (для вопросов с открытым ответом)
class OpenAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, limit_choices_to={'question_type': 'open'})
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self):
        return f'Answer by {self.user.username} for question {self.question.text}'
    
    class Meta:
        verbose_name = 'Открытый ответ'
        verbose_name_plural = 'Открытые ответы'


# Результаты теста пользователя
class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    passed = models.BooleanField(default=False)
    score = models.FloatField(default=0.0)
    attempt_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.test.title} - {"Passed" if self.passed else "Failed"}'
    
    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'


# Финальный тест по курсу
class FinalTest(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)  # Вопросы финального теста

    def __str__(self):
        return f"Final Test for {self.course.title}"
    
    class Meta:
        verbose_name = 'Финальный тест'
        verbose_name_plural = 'Финальные тесты'


# Результаты финального теста
class FinalTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    final_test = models.ForeignKey(FinalTest, on_delete=models.CASCADE)
    passed = models.BooleanField(default=False)
    score = models.FloatField()
    attempt_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.user.username} - Final Test {self.final_test.course.title} - {"Passed" if self.passed else "Failed"}'
    
    class Meta:
        verbose_name = 'Результат финального теста'
        verbose_name_plural = 'Результаты финальных тестов'
