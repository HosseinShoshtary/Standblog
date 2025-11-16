from django import forms


class ContactUsForm(forms.Form):
    text = forms.CharField(max_length=500, label="your massege")
