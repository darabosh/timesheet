from django import forms

class UpdateForm(forms.Form):
    member_name = forms.CharField(label='Member name:', max_length=30,
                                    widget=forms.TextInput(attrs={'class': 'in-text'}))
    username = forms.CharField(label='Username:', max_length=30,
                                    widget=forms.TextInput(attrs={'class': 'in-text'}))
    email = forms.EmailField(label='Email:', max_length=30,
                                    widget=forms.TextInput(attrs={'class': 'in-text'}))
    hours_per_week = forms.DecimalField(label='Hours per week:',
                                    widget=forms.TextInput(attrs={'class': 'in-text'}))
    status = forms.CharField()
    role = forms.CharField()
    pk = forms.IntegerField(label='Pk:', widget=forms.TextInput(attrs={'class': 'in-text'}))