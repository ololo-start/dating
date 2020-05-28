from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, ListView, UpdateView
from accounts.forms import UserProfileEditForm, UserEditForm
from accounts.models import  UserLike


@login_required
def login_redirect(request):
    return redirect('profile', pk=request.user.id)


class Start(TemplateView):
    template_name = 'start.html'


@login_required
def user_profile_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'profile.html', context={
        'user': user,
        'selected_user': request.user
    })


class EditProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'edit.html'
    user_form = UserEditForm
    profile_form = UserProfileEditForm

    def get(self, request, *args, **kwargs):
        self.user_form = UserEditForm(instance=request.user)
        self.profile_form = UserProfileEditForm(instance=request.user.userprofile)
        return render(request, self.template_name, context={
            'user_form': self.user_form,
            'profile_form': self.profile_form
        })

    def post(self, request, *args, **kwargs):
        self.user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        self.profile_form = UserProfileEditForm(instance=request.user.userprofile,
                                       data=request.POST,
                                       files=request.FILES)
        if self.user_form.is_valid() and self.profile_form.is_valid():
            self.user_form.save()
            self.profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error')
        return render(request, self.template_name, {
            'user_form': self.user_form,
            'profile_form': self.profile_form
        })


class PeopleList(LoginRequiredMixin, ListView):
    template_name = 'people_list.html'
    paginate_by = settings.PAGE_SIZE

    def get_queryset(self):
        return User.objects.filter(
            userprofile__gender=self.request.user.userprofile.partner_gender).filter(
            userprofile__age=self.request.user.userprofile.partner_age).filter(
            userprofile__orientation=self.request.user.userprofile.partner_orientation).exclude(
            username=self.request.user).exclude(
            userlike__voter=self.request.user).\
            select_related('userprofile')


@login_required
def create_like(request, pk, vote):
    user = get_object_or_404(User, pk=pk)
    UserLike.objects.create(
        to_user=user, voter=request.user, like=vote)
    return redirect('people')


@login_required
def like(request, pk):
    return create_like(request, pk, True)


@login_required
def dislike(request, pk):
    return create_like(request, pk, False)


@login_required
def pair(request):
    your_like = UserLike.objects.filter(
        voter=request.user, like=True
    ).values('to_user')
    like_you = UserLike.objects.filter(
       to_user=request.user, like=True
    ).filter(
        voter__in=your_like
    )
    return render(request, 'pair.html', context={
        'partners': like_you,
    })

