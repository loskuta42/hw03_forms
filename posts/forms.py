from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import Post
from django import forms

User = get_user_model()


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']

    def validate_not_empty(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError(
                'А кто пост будет писать, Пушкин?',
                params={'data': data},
            )
        return data
