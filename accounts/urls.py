from django.conf import settings
from django.urls import path
from accounts import views
from accounts.views import Start, PeopleList, EditProfileView
from django.conf.urls.static import static



urlpatterns = [
    path('',  Start.as_view(), name='start'),
    path('login_redirect', views.login_redirect, name='login_redirect'),
    path('edit', EditProfileView.as_view(), name='edit'),
    path('people', PeopleList.as_view(), name='people'),
    path('profile/<int:pk>', views.user_profile_view, name='profile'),
    path('profile/<int:pk>/like', views.like, name='like'),
    path('profile/<int:pk>/dislike', views.dislike, name='dislike'),
    path('pair', views.pair, name='pair')
        ]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)