from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'group': 'Выберите группу',
            'text': 'Введите текст'
        }
        help_texts = {
            'group': 'Группа поста',
            'text': 'Текст записи'
        }
