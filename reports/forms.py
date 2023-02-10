from django import forms


class ReportForm(forms.Form):
    member = forms.ChoiceField(label='Team Member:', required=False)
    client = forms.ChoiceField(label='Client:', required=False)
    project = forms.ChoiceField(label='Project:', required=False)
    category = forms.ChoiceField(label='Category:', required=False)
    start_date = forms.DateField(required=False, widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': "in-text datepicker hasDatepicker"}))
    end_date = forms.DateField(required=False, widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': "in-text datepicker hasDatepicker"}))