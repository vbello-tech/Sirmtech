from django import forms
from .models import Nysc


class NyscForm(forms.ModelForm):
    class Meta:
        model = Nysc
        fields = (
            'first_name',
            'last_name',
            'other_name',
            'email',
            'capturing',
            'call_up',
            'passport',
            'medical_certificate',
            'concord_printing',
            )
        labels = {
            'capturing': 'Service Charge - (₦3000)',
            'call_up': 'Call Up Letter - (₦3500)',
            'passport': 'Passport Photography - 12 pieces (₦1000)',
            'medical_certificate': 'Medical Fitness Certificate - (₦1500)',
            'concord_printing': 'Concord Medical Printing - (₦500)',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none '
                         'focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none '
                         'focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter Last Name'
            }),
            'other_name': forms.TextInput(attrs={
                'class': 'form-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none '
                         'focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter other Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none '
                         'focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter Email Address',
                'required': True,
            }),
            'capturing': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600 rounded focus:ring-blue-500',
                'required': True,
            }),
            'call_up': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600 rounded focus:ring-blue-500',
                'required': True,
            }),
            'passport': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600 rounded focus:ring-blue-500'
            }),
            'medical_certificate': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600 rounded focus:ring-blue-500'
            }),
            'concord_printing': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600 rounded focus:ring-blue-500'
            })
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Add red * to label if field is required
            for name, field in self.fields.items():
                if field.required:
                    field.label = f'{field.label} <span style="color:red;">*</span>'
