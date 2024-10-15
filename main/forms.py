from django import forms
from .models import Course, Article, Question, Answer, FinalTest


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['category', 'title', 'description']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        #fields = ['text', 'is_final_question']
        fields = ['text', 'question_type']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']


class FinalTestForm(forms.ModelForm):
    class Meta:
        model = FinalTest
        fields = ['questions']

# class Test(forms.ModelForm):
#     class Meta:
#         model = Test
#         fields = ['article', 'title']