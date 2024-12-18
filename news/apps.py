"""
This module provides app configuration for news.
Django uses this configuration to set up and manage application-specific settings.
"""
from django.apps import AppConfig


class NewsConfig(AppConfig):
    """
    This class specifies the default primary key field type and the app name
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
