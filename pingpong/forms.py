from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from pingpong.validators import Validator
from pingpong.models import UserProfile


class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        widgets = {
            'username': forms.TextInput(attrs={'placeholder':'Username'}),
            'email': forms.EmailInput(attrs={'placeholder':'john.doe@hds.com'}),
            'password': forms.PasswordInput(attrs={'placeholder':'Password'}),
            }

    # overriding ModelForm clean() method used by is_valid()
    def clean(self):
        data = self.cleaned_data
        validate = Validator()
        # calls cleaned_data from ModelForm to retreive fields
        username = validate.username(data.get('username'))
        email = validate.email(data.get('email'))
        password = validate.password(data.get('password'), data.get('confirm_password'))
        # raise Validation errors
        if email or password:
            raise ValidationError([username, email, password,])
        else:
            return data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)