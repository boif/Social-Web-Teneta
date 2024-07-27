from django.urls import path
from Chat import views

urlpatterns = [
    path('createChat/', views.create_chat, name='create_chat'),
    path('<int:chat_id>/', views.chat_detail, name='chat_detail'),
]