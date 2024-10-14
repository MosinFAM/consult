from django.db import models
from django.contrib.auth.models import User
from users.models import Profile


class Course(models.Model):
    title = models.CharField(max_length=255)

class Article(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='articles')

class Test(models.Model):
    title = models.CharField(max_length=255)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='tests')

class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('text', 'Text'),
    ]
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text_description = models.CharField(max_length=255)
    text_task = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

class TestResult(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='test_results')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    best_score = models.IntegerField(default=0)

class OpenAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='open_answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='open_answers')
    answer_text = models.TextField()
