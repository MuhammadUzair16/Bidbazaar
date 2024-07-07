from django import forms
from .models import Account

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
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'address' ,'dob']

    widgets = {
        'dob': forms.SelectDateWidget(years=range(1900, 2100)),
    }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password and Confirm Password do not match")
        return cleaned_data