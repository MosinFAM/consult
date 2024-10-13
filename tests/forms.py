from django import forms
from .models import Question, AnswerOption

class TestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)

        for question in questions:
            if question.question_type == Question.SINGLE_CHOICE:
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    choices=[(option.id, option.text) for option in question.options.all()],
                    widget=forms.RadioSelect,
                    label=question.text,
                    required=True
                )
            elif question.question_type == Question.MULTIPLE_CHOICE:
                self.fields[f'question_{question.id}'] = forms.MultipleChoiceField(
                    choices=[(option.id, option.text) for option in question.options.all()],
                    widget=forms.CheckboxSelectMultiple,
                    label=question.text,
                    required=True
                )
            elif question.question_type == Question.TEXT_ANSWER:
                self.fields[f'question_{question.id}'] = forms.CharField(
                    widget=forms.Textarea,
                    label=question.text,
                    required=True
                )
