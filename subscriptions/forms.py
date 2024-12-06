from django import forms
from django.contrib.auth.models import User

class SignupForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15)
    terms_accepted = forms.BooleanField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def clean_terms_accepted(self):
        terms_accepted = self.cleaned_data.get('terms_accepted')
        if not terms_accepted:
            raise forms.ValidationError('You must accept the terms and conditions.')
        return terms_accepted
