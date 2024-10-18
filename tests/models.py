from django.db import models
from django.contrib.auth.models import User
from main.models import Article, Course
from users.models import Profile


    
# Тест для статьи
class Test(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Test {self.order} for {self.article.title}'

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['order']


# Вопрос
class Question(models.Model):
    OPEN = 'open'
    CHOICE = 'choice'

    QUESTION_TYPES = [
        (OPEN, 'Open-ended'),
        (CHOICE, 'Multiple choice'),
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text_description = models.TextField() #само задание
    text_task = models.TextField() #содержание задания
    question_type = models.CharField(max_length=17, choices=[('multiple_choice', 'Multiple Choice'), ('text', 'Text')])
    
    def __str__(self):
        return f'{self.text_task}'

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


# Вариант ответа
class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return  f'{self.text}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

# Открытые ответы пользователя (для вопросов с открытым ответом)
class OpenAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, limit_choices_to={'question_type': 'open'})
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self):
        return f'Answer by {self.user.username} for question {self.question}'
    
    # def __str__(self):
    #     return f'Answer by {self.user.username} for question {self.question.text}'

    class Meta:
        verbose_name = 'Открытый ответ'
        verbose_name_plural = 'Открытые ответы' 




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





class TestResult(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()  # Количество правильных ответов
    total_questions = models.IntegerField()  # Общее количество вопросов
    passed = models.BooleanField(default=False)

    answer_text = models.TextField(null=True, blank=True, default=" ")

    def __str__(self):
        return f"{self.profile.user.username} - {self.test.title} - {self.score}"

    class Meta:
        verbose_name = 'Результат теста'
        verbose_name_plural = 'Результаты тестов'





# Модель для связи теста и курса (или статьи)
class Enrollment(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test.title} тест от  {self.article.title}"

