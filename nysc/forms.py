from django import forms
from .models import Nysc


class NyscForm(forms.ModelForm):
    class Meta:
        model = Nysc
        fields = (
            'first_name',
            'last_name',
            'email',
            'capturing',
            'passport',
            'medical_certificate',
            )

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none '
                         'focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none '
                         'focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter First Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none '
                         'focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter Email Address',
                'required': True,
            }),
            'capturing': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600 rounded focus:ring-blue-500'
            }),
            'passport': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600 rounded focus:ring-blue-500'
            }),
            'medical_certificate': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600 rounded focus:ring-blue-500'
            })
        }
