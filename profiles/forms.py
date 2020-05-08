from django import forms
from django.contrib.auth.models import User
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']



class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['photo','contact_email','phone_number']



