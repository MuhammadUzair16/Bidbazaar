from datetime import datetime, date
from django import forms
from .models import Account
import re

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        {
           'placeholder': 'Enter Password'
        }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        {
            'placeholder': 'Confirm Password'
        }))
    dob = forms.DateField(widget=forms.SelectDateWidget(
        years=range(1900, 2100),
        attrs={
            'class': 'dob-select'
        }
    ))
    address = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'placeholder': 'Enter Address',
            'class': 'address-input'
        }
    ))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'address', 'dob']
        widgets = {
            'dob': forms.SelectDateWidget(years=range(1900, 2100)),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')


        if not re.search(r'[A-Za-z]', email):
            raise forms.ValidationError("Email must contain at least one alphabetic character.")


        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise forms.ValidationError("Enter a valid email address.")


        if email.endswith('@gmail.com'):
            local_part = email.split('@')[0]
            if not re.search(r'[A-Za-z]', local_part):
                raise forms.ValidationError(
                    "The part before '@gmail.com' must contain at least one alphabetic character.")

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Za-z]', password):
            raise forms.ValidationError("Password must contain at least one alphabetic character.")
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("Password must contain at least one numeric character.")
        if not re.search(r'[@$!%*?&]', password):
            raise forms.ValidationError("Password must contain at least one special character (@, $, !, %, *, ?, &).")
        return password

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only numeric characters.")
        return phone_number

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("First name must contain only alphabetic characters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Last name must contain only alphabetic characters.")
        return last_name

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password and Confirm Password do not match.")
        return cleaned_data

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')

        if dob and dob > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future.")

        return dob

