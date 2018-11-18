from django import forms
from django.conf import settings
from django.contrib.auth import password_validation
import re
from .models import User, UserProfile
from users.models import USER_ROLES

class RegisterForm(forms.ModelForm):
    """
    Form to register a new user
    """
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '','required':'required'}),
        strip=False,
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '','required':'required'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
            'password',
            'confirm_password'
        ]
        widgets = {
          
            'full_name': forms.TextInput(attrs={'class': 'form-control','required':'required', 'placeholder': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '','required':'required'}),
            
        }

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        
        full_name = self.cleaned_data['full_name']

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password mismatch')
        if full_name.lower() in password.lower():
            raise forms.ValidationError('Password similar to name of user.')
        password_validation.validate_password(confirm_password, self.instance)
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not re.match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email):
            raise forms.ValidationError('Invalid Email format')
        return email

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """
    Form to login a user
    """
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'class': 'form-control','required':"required", 'placeholder':" "}),
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control','required':"required", 'placeholder':" "}),
        strip=False,
    )

    def clean_(self):
        email= self.cleaned_data.get('')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

        if user:
            return user.email
        return None


class PasswordChangeForm(forms.Form):
    """
    Form to change user password
    """
    current_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your current password'}),
        strip=False,
    )

    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your new password'}),
        strip=False,
    )

    confirm_new_password = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your new password password'}),
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data["current_password"]
        if not self.user.check_password(current_password):
            raise forms.ValidationError('Incorrect current password')
        return current_password

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data['new_password']
        confirm_new_password = self.cleaned_data['confirm_new_password']
        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                raise forms.ValidationError('Password mismatch')
        password_validation.validate_password(confirm_new_password, self.user)
        return confirm_new_password

    def save(self, commit=True):
        password = self.cleaned_data["confirm_new_password"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class PasswordResetForm(forms.Form):
    """
    Form to reset user's password
    """
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your new password'}),
        strip=False,
    )

    confirm_new_password = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your new password password'}),
        strip=False,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data['new_password']
        confirm_new_password = self.cleaned_data['confirm_new_password']
        if new_password and confirm_new_password:
            if new_password != confirm_new_password:
                raise forms.ValidationError('Password mismatch')
        return confirm_new_password

    def save(self):
        password = self.cleaned_data["confirm_new_password"]
        self.user.set_password(password)
        self.user.save()
        return self.user


class GuestForm(forms.Form):
    email = forms.EmailField()



class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
           'address_line_1',
           'address_line_2',
           'gender',
           'pic',
           'city',
           'postal_code',
           'country'
        ]
        widgets = {
          
            'address_line_1': forms.TextInput(attrs={'class': 'form-control','required':'required', 'placeholder': ''}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control','required':'required', 'placeholder': ''}),
            'gender': forms.Select(attrs={'class': 'form-control','required':'required', 'placeholder': ''}),
            'city': forms.TextInput(attrs={'class': 'form-control','required':'required', 'placeholder': ''}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control','required':'required', 'placeholder': ''}),
            'country': forms.TextInput(attrs={'class': 'form-control','required':'required', 'placeholder': ''}),

        }