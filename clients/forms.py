from django import forms

COUNTRY_CHOICES = [
    ("us", "us"),
    ("uk", "uk"),
    ("serbia", "serbia"),
    ("china", "china"),
]

class UpdateForm(forms.Form):
    client_name = forms.CharField(label='Client name:', max_length=30,
                                    widget=forms.TextInput(attrs={'class': 'in-text'}))
    address = forms.CharField(label='Address:', max_length=30,
                                    widget=forms.TextInput(attrs={'class': 'in-text'}))
    city = forms.CharField(label='City:', max_length=30,
                                    widget=forms.TextInput(attrs={'class': 'in-text'}))
    zip = forms.IntegerField(label='Zip/Postal code:',
                                    widget=forms.TextInput(attrs={'class': 'in-text'}))
    country = forms.ChoiceField(choices=COUNTRY_CHOICES)
    pk = forms.IntegerField(label='Pk:', widget=forms.TextInput(attrs={'class': 'in-text'}))