# models.py
from django.db import models

class ChatSession(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Chat {self.id}: {self.title or 'Untitled'}"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    sender_type = models.CharField(max_length=50, default='user')  # 'user' or 'assistant'
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender_type} message in {self.session}"

    class Meta:
        ordering = ['created_at']