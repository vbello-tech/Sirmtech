from django import forms
from .models import Nysc


class NyscForm(forms.ModelForm):
    class Meta:
        model = Nysc
        fields = ('first_name', 'last_name', 'email', 'capturing', 'passport', 'medical',)

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    "placeholder": 'Your first name?',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    "placeholder": 'Your last name?',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
,                   "placeholder": 'Input email',
                }
            ),
            'capturing': forms.CheckboxInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'passport': forms.CheckboxInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'medical': forms.CheckboxInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }