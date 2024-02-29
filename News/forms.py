from django import forms
from News.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'text', 'content']
