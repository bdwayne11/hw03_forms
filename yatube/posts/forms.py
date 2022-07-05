from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea,
        label='Введите текст',
        required=True,
        help_text='Текст поста'
    )

    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {'group': 'Выберите группу'}
        help_texts = {
            'group': 'Группа поста'
        }

    def clean_subject(self):
        data = self.cleaned_data['text']
        if len(data) == 0:
            raise forms.ValidationError('В записи должен быть текст!')
        return data
