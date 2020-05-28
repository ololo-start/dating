from django.conf import settings
import time
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from chat.models import Message, Chat


@shared_task
def new_message(message_id, message_author, chat_id):
    time.sleep(3600)
    message = Message.objects.filter(is_read=False).filer(id=message_id).first()
    if message:
        chat = Chat.objects.get(id=chat_id)
        members_ids = chat.values_list('members__id', flat=True)
        for member in members_ids:
            if member != message_author:
                user = User.objects.get(id=member)
                email_message = f'Hi {user.first_name}! You have new message ' \
                                f'from {message.author}:\n  {message.message}\n'
                send_mail(
                    subject='New message',
                    message=email_message,
                    from_email=settings.ADMIN_EMAIL,
                    recipient_list=[user.email]
                )


