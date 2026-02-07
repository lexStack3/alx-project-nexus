from django import forms


class CustomSignupForm(forms.Form):
    """
    Custom sign-up form for addition fields.
    """
    first_name = forms.CharField(
        max_length=128,
        label='First Name',
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=128,
        label='Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )

    def signup(self, request, user):
        """
        Called after user is created but before saved to handle additional fields
        """
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone = self.cleaned_data.get('phone', '')

        user.save()
