
from django.urls import path

from registration.views import RegistrationView

urlpatterns = [

    path('signup', RegistrationView.as_view(), name='signup')
    ]