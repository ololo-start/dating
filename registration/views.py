from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from registration.forms import RegistrationForm
from django.views.generic import FormView


class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('edit')

    def form_valid(self, form):
        form.save()
        user = authenticate(
            self.request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        return super().form_valid(form)


