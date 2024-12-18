from django.urls import path
from news import views
from django.conf.urls.static import static
from django.conf import settings

"""
This module defines the url patterns for the news app.

Routes:
    - '' : creating post on the home page.
    - 'post/<int:pk>/' : updating post.
    - 'post/<int:pk>/delete/' : deleting post.
    - 'like/<int:post_id>/' : like post.
    - 'comment/<int:post_id>/' : comment post.
"""

urlpatterns = [
    path('', views.createPost, name='home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post'),
    path('post/<int:pk>/update', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post_delete'),
    path('like/<int:post_id>/', views.likePost, name='like_post'),
    path('comment/<int:post_id>/', views.commentPost, name='add_comment'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)