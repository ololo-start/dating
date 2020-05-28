from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from chat.forms import MessageForm
from chat.models import Chat
from chat.tasks import new_message
from dating import settings


@login_required
def get_all_chats(request):
    chats = Chat.objects.filter(members__in=[request.user.id])
    return render(request, 'all_chats.html', context={
        'user': request.user, 'chats': chats})


class MessagesView(LoginRequiredMixin, View):
    def get(self, request, pk):
        chat = Chat.objects.get(id=pk)
        if request.user in chat.members.all():
            chat.messages.filter(is_read=False).exclude(author=request.user).update(is_read=True)
        else:
            chat = None
        chat_messages = chat.messages.all()
        paginator = Paginator(chat_messages, settings.PAGE_SIZE_MESSAGE,  orphans=settings.PAGE_SIZE_MESSAGE)
        page = request.GET.get('page', paginator.num_pages)
        chat_messages = paginator.get_page(page)
        return render(
            request, 'chat.html', context={
                'user': request.user,
                'chat': chat,
                'chat_messages': chat_messages,
                'form': MessageForm()})

    def post(self, request, pk):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = pk
            message.author = self.request.user
            message.save()
            #new_message.delay(message.id, message.author, message.chat_id)
        return redirect(reverse('messages', kwargs={'pk': pk}))


class CreateDialogView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        member = [user_id, self.request.user.id]
        chat = Chat.objects.filter(members__in=member).annotate(num_attr=Count('members')).filter(num_attr=2).first()
        if not chat:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        return redirect(reverse('messages', kwargs={'pk': chat.id}))
