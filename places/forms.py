from django.forms import (

    ModelForm, HiddenInput, ValidationError
)

from places.models import Place, Media ,Review
from django import forms


class PlaceCreationForm(ModelForm):
    class Meta:
        model=Place
        fields=(
            'name',
            'coordinates',
            'category',
            'has_wifi',
            'telephone',
            'description',
        )

        widgets ={
            'coordinates': HiddenInput,
            'category': forms.Select(attrs={'class': 'form-control'}),
            'has_wifi': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ('Place Name')
            }
            ),

            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':('Telephone')
            }
            ),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': ('Enter a description')
            }
            )
        }

    def clean_coordinates(self):
        coords = self.cleaned_data['coordinates']

        try:
            lat, lng = coords.split(',')
            lat = float(lat)
            lng = float(lng)

            if (
                    lat < -90 or lat > 90 or
                    lng < -180 or lng > 180
            ):
                raise ValidationError('Geçerli bir koordinat girin.')


        except ValueError:
            raise ValidationError('Koordinat girin.')

        return coords

class MediaCreationForm(ModelForm):
    class Meta:
        model=Media
        fields=("image",)

class ReviewCreationForm(ModelForm):
    class Meta:
        model=Review
        fields=("comment",
                "vote",)
