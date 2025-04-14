from django.urls import path
from . import views

urlpatterns = [
    path('chat/sessions/', views.chat_sessions, name='chat_sessions'),
    path('chat/sessions/<int:session_id>/messages/', views.chat_messages, name='chat_messages'),
    path('chat/sessions/<int:session_id>/assistant-response/', views.get_assistant_response, name='get_assistant_response'),
]
