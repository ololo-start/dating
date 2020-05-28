from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        strip=False, label='Password',
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',  'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError("This email address already exists")
        except User.DoesNotExist:
            return email

