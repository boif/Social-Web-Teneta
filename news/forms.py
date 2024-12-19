"""
This module defines the forms used in the news app.
"""

from django import forms
from news.models import Post

class PostForm(forms.ModelForm):
    """
    Form for creating and updating posts.
    """
    class Meta:
        """
        Meta options for the PostForm
        """
        model = Post
        fields = ['text', 'content']
