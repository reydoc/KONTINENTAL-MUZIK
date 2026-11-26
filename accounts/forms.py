from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


class ArtistRegistrationForm(forms.Form):

    full_name = forms.CharField(max_length=150)

    artist_name = forms.CharField(max_length=150)

    username = forms.CharField(max_length=150)

    email = forms.EmailField()

    password1 = forms.CharField(
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                'This username is already taken.'
            )

        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'This email is already registered.'
            )

        return email

    def clean_password1(self):
        password = self.cleaned_data['password1']

        try:
            validate_password(password)
        except ValidationError as error:
            raise forms.ValidationError(error.messages)

        return password

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error(
                'password2',
                'The passwords do not match.'
            )

        return cleaned_data
