from django.forms import ModelForm
from django import forms
from chat.models import Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Type a message',
                                             'rows': 2, 'cols': 45})
        }