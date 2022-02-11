from django import forms
# from nlp.models import Review

class ReviewForm(forms.Form):
    review = forms.CharField(max_length=300)  # QuestionForm에서 사용할 Question 모델의 속성
