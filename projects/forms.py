from django import forms


class UpdateForm(forms.Form):
    project_name = forms.CharField(label='Project name:', max_length=30,
                                    widget=forms.TextInput(attrs={'class': 'in-text'}))
    description = forms.CharField(label='Description:', max_length=30,
                                    widget=forms.TextInput(attrs={'class': 'in-text'}))
    customer = forms.ChoiceField(label='Customer:')
    lead = forms.ChoiceField(label='Customer:')
    archive = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    pk = forms.IntegerField(label='Pk:', widget=forms.TextInput(attrs={'class': 'in-text'}))