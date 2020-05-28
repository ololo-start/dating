from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    members = models.ManyToManyField(User, related_name='chats')

    def get_members(self):
        return ",".join([str(member) for member in self.members.all()])


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return self.message
