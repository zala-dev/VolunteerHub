from django import forms

class DonationForm(forms.Form):
    amount = forms.IntegerField(label="Donation Amount $:", min_value=1)
