"""
This module defines the models used in the news app.

Models:
    - Post
    - Like
    - Comment
"""

from django.db import models
from django.contrib.auth import get_user_model

class Post(models.Model):
    """
    Represents a news post.
    """
    User = get_user_model()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField(blank=True)
    content = models.FileField(
        upload_to='PostContent',
        blank=True,
        null=True)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True,
        through='Like'
    )

    def __str__(self):
        """
        Returns a string representation of the post.
        """
        return f"{self.author.username} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"

    def get_absolute_url(self):
        """
        Returns the url to access a particular post.
        """
        return f'/post/{self.id}'

class Like(models.Model):
    """
    Represents a like for post.
    """
    User = get_user_model()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    """
    Represents a comment for post.
    """
    User = get_user_model()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    parent_comment = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='replies'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the comment.
        """
        return (
            f"{self.user.username} - {self.post.id} "
            f"{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        )
