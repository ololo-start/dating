from django.urls import path
from chat import views
from chat.views import MessagesView, CreateDialogView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('chat', views.get_all_chats, name='chats'),
    path('chat/create/<int:user_id>', CreateDialogView.as_view(),  name='create_chat'),
    path('chat/<int:pk>', MessagesView.as_view(), name='messages')
    ]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
