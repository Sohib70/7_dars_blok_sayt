
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# class SignUpForm(forms.ModelForm):
#     password1 = forms.CharField(label='Parol',widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Parol', widget=forms.PasswordInput)
class SignUpForm(forms.ModelForm):
    new_pass = forms.CharField(widget=forms.PasswordInput, label="Parol")
    confirm_pass = forms.CharField(widget=forms.PasswordInput, label="Parolni tasdiqlang")
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']


    # def clean_password1(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #     if password1 is None or password2 is None or password1 != password2:
    #         raise forms.ValidationError('Parollar tugri kelmadi')
    #     return password1
    def clean(self):
        cleaned_data = super().clean()
        new_pass = self.cleaned_data.get('new_pass')
        confirm_pass = self.cleaned_data.get('confirm_pass')
        if new_pass != confirm_pass:
            raise forms.ValidationError('Parollar mos emas')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['new_pass'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,label='login')
    password = forms.CharField(label='Parol',widget=forms.PasswordInput)

class ChangePassForm(forms.Form):
    old_pass = forms.CharField(label='Eski parol',widget=forms.PasswordInput)
    new_pass = forms.CharField(label='Yangi parol', widget=forms.PasswordInput)
    confirm_pass = forms.CharField(label='Parolni tasdiqlang', widget=forms.PasswordInput)
    code = forms.CharField(label='kodni kiriting', max_length=6)