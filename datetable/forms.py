from django import forms


class TimeslotForm(forms.Form):
    client = forms.ChoiceField(label='Client:', required=False)
    project = forms.ChoiceField(label='Project:', required=False)
    description = forms.CharField(max_length=300, required=False, widget=forms.TextInput(attrs={'class': 'in-text medium'}))
    time = forms.DecimalField(max_digits=3, required=False, decimal_places=1, label='Time:', widget=forms.TextInput(attrs={'class': 'in-text xsmall'}))
    overtime = forms.DecimalField(max_digits=3, required=False, decimal_places=1, label='Overtime:', widget=forms.TextInput(attrs={'class': 'in-text xsmall'}))
    pk = forms.IntegerField(label='Pk:', required=False, widget=forms.TextInput(attrs={'class': 'in-text'}))