from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django import forms

class RegistrationForm(UserCreationForm):
    class Meta:
        fields=["username","email"]

        widgets ={
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ('E-Mail')}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':('Username')}),
        }

        password1= forms.PasswordInput(attrs={'class': 'form-control'})
        password2=forms.PasswordInput(attrs={'class': 'form-control'})

        model =User

class LoginForm(forms.Form):
    username = forms.CharField(required=True,
                               label='',
                               widget=forms.TextInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': ('Username')
                                                            }
                                                     )
                               )
    password = forms.CharField(required=True,
                               label='',
                               widget=forms.PasswordInput(attrs={
                                                                    'class' : 'form-control',
																    'placeholder' : ('Password')
																}
                                                          )
                               )

    def clean(self):
        username=self.cleaned_data.get("username")
        password= self.cleaned_data.get("password")
        if not username or not password:
            return self.cleaned_data

        user=authenticate(username=username,   #session oluşturup kullanıcı bilgilerini tutuyoruz
                          password=password)

        if user:
            self.user=user
        else:
            raise ValidationError("Yanlış kullanıcı adı veya şifre!")

        return self.cleaned_data
