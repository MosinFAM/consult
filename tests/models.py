from django.db import models
from main.models import Article
from django.contrib.auth.models import User

class Test(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Question(models.Model):
    SINGLE_CHOICE = 'single'
    MULTIPLE_CHOICE = 'multiple'
    TEXT_ANSWER = 'text'

    QUESTION_TYPES = [
        (SINGLE_CHOICE, 'Один правильный ответ'),
        (MULTIPLE_CHOICE, 'Несколько правильных ответов'),
        (TEXT_ANSWER, 'Свободный ответ'),
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)

    def __str__(self):
        return self.text

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField()
    is_passed = models.BooleanField()

    def __str__(self):
        return f'{self.user.username} - {self.test.title} - {self.score}'
