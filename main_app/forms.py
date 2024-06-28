from django import forms

class DonationForm(forms.Form):
    amount = forms.IntegerField(label="Amount", min_value=0)
