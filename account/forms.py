
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Parol',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Parol', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 is None or password2 is None or password1 != password2:
            raise forms.ValidationError('Parollar tugri kelmadi')
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,label='login')
    password = forms.CharField(label='Parol',widget=forms.PasswordInput)