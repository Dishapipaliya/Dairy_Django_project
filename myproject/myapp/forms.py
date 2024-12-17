from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm,SetPasswordForm,PasswordResetForm
from .models import Customer
from django.contrib.auth.models import User



class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    password = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

class CustomRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1=forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm password',widget=forms.PasswordInput(attrs={'class':'form-control'})) 

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

        
class MyPasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(label='Old Password',widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password','class':'form-control'}))
    new_password1=forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password','class':'form-control'}))
    new_password2=forms.CharField(label='Confirm password',widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password','class':'form-control'}))


  # Assuming you want to use the Customer model

class CustomerProfileForm(forms.ModelForm):  # Add the missing colon here
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'mobile', 'zipcode', 'state']  # List the fields you want to include
        widgets={                                
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
        }


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1=forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password','class':'form-control'}))
    new_password2=forms.CharField(label='Confirm New Password',widget=forms.PasswordInput(attrs={'autofocus':'True','autocomplete':'current-password','class':'form-control'}))