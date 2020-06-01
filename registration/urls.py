
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from registration.views import RegistrationView

urlpatterns = [

    path('signup', RegistrationView.as_view(), name='signup')
    ]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
