from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


#https://www.reddit.com/r/webdev/comments/cjfmg8/django_deleting_user_accounts/?st=k58rsdiu&sh=655d06bf
class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []   #Form has only submit button.  Empty "fields" list still necessary, though.



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

