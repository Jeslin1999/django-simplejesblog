from django.forms import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User,Post
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError



class LoginForm(AuthenticationForm):
    username = CharField(
        max_length = 15,
        min_length = 3,
        label = 'Username',
        required = True,
        widget = TextInput({
            'class' : 'form-control'
        })
    )
    
    password = CharField(
        max_length = 15,
        min_length = 4,
        label = 'Password',
        required = True,
        widget = PasswordInput({
            'class' : 'form-control'
        })
    )
    class Meta:
        model = User
        fields = ('username','password')

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
        'class': 'border border-gray-300 rounded-md p-2 w-full'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter your username',
                'class': 'border border-gray-300 rounded-md p-2 w-full'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Enter your password',
                'class': 'border border-gray-300 rounded-md p-2 w-full'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Confirm your password',
                'class': 'border border-gray-300 rounded-md p-2 w-full'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email'] 


class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            fields = ['title', 'content', 'tags']
            widgets = {
                'title': forms.TextInput(attrs={
                    'class': 'block w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                    'placeholder': 'Enter post title'
                }),
                'tags': forms.SelectMultiple(attrs={
                    'class': 'block w-full mt-1 px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
                })
            }