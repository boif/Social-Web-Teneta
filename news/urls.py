"""
This module defines the url patterns for the news app.

Routes:
    - '' : creating post on the home page.
    - 'post/<int:pk>/' : updating post.
    - 'post/<int:pk>/delete/' : deleting post.
    - 'like/<int:post_id>/' : like post.
    - 'comment/<int:post_id>/' : comment post.
"""

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from news import views

urlpatterns = [
    path('', views.create_post, name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post'),
    path('post/<int:pk>/update', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post_delete'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.comment_post, name='add_comment'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
