# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Quiz, Question, AnswerOption

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['quiz_title', 'quiz_description', 'total_marks', 'time_limit']
        widgets = {
            'time_limit': forms.NumberInput(attrs={'placeholder': 'Time limit (minutes)'}),  
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'points']

class AnswerOptionForm(forms.ModelForm):
    class Meta:
        model = AnswerOption
        fields = ['option_text', 'is_correct']

# Formset for multiple questions
QuestionFormSet = inlineformset_factory(
    Quiz, Question, form=QuestionForm, extra=1, can_delete=True
)
