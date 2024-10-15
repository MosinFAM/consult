from django import forms
from .models import Test, FinalTest

class Test(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['article', 'title']

