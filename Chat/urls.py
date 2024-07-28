from django.urls import path
from Chat import views

urlpatterns = [
    path('chat/start/<str:username>/', views.start_chat, name = 'start_chat'),
    path('chat/<int:chat_id>/', views.chat_detail, name = 'chat_detail'),
]