from django import forms
from .models import Questions


class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ('asked_by', 'course', 'subject', 'heading', 'question',
                  'ques_img')
