from django.forms import (

    ModelForm, HiddenInput, ValidationError
)
from activities.models import Activity, Media ,Review
from django import forms

class ActivityCreationForm(ModelForm):
    class Meta:
        model=Activity
        fields=(
            'name',
            'route',
            'category',
            'is_active',
            'telephone',
            'description',

        )

        widgets ={

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ('Etkinlik Adı')
            } ),

            'route': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ('Rota')
            } ),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': ('Açıklama Girin')
            }
            ),

            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-control'}),


            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':('Telefon')
            }
            )
        }


class MediaCreationForm(ModelForm):
    class Meta:
        model=Media
        fields=("image",)

class ReviewCreationForm(ModelForm):
    class Meta:
        model=Review
        fields=("comment",)
