from django import forms
from news.models import Post

"""
This module defines the forms used in the news app.
"""

class PostForm(forms.ModelForm):
    """
    Form for creating and updating posts.
    """
    class Meta:
        model = Post
        fields = ['text', 'content']
