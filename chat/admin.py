from django.contrib import admin
from chat.models import Chat, Message


class MessageInline(admin.StackedInline):
    model = Message
    can_delete = False
    verbose_name_plural = 'message'


class ChatAdmin(admin.ModelAdmin):
    list_display = ('get_members',)
    inlines = (MessageInline, )


admin.site.register(Chat, ChatAdmin)
