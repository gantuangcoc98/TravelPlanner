from django import forms
from .models import User

class UserLogin(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    
        
class UserRegistration(forms.Form):
    username = forms.CharField(widget=forms.TextInput, label='username')
    email = forms.CharField(widget=forms.TextInput, label='email')
    password = forms.CharField(widget=forms.PasswordInput, label='password')
    first_name = forms.CharField(widget=forms.TextInput, label='first_name')
    last_name = forms.CharField(widget=forms.TextInput, label='last_name')
    contact_number = forms.IntegerField(widget=forms.NumberInput, label='contact_number')
    
    class Meta:
        model = User
        field = ['username', 'email', 'password', 'first_name', 'last_name', 'contact_number']
