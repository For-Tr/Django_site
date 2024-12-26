from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from .models import ParkingSpace
from django import forms
from django.forms.widgets import PasswordInput, TextInput



class CreateUserForm(UserCreationForm):


    group  = forms.ModelChoiceField(queryset=Group.objects.all(), widget=forms.Select , required=True)


    class Meta:


        model = User
        fields = ['username', 'email', 'password1', 'password2', 'group']



class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class ParkingSpaceForm(forms.ModelForm):
    class Meta:
        model = ParkingSpace
        fields = ['location', 'availability', 'hourly_price']
        labels = {
            'location': '物品名称',
            'availability': '是否可领取',
            'hourly_price': '价值',
        }
