from django import forms
from django.core.validators import ValidationError
from blog.models import Message


class ContactUsForm(forms.Form):
    BIRTH_YEAR_CHOICES = ["2000", "2003", "2007"]
    FAVORITE_COLOR_CHOICES = [
        ("blue", "Blue"),
        ("green", "Green"),
        ("red", "Red"),
        ("black", "Black")
    ]
    name = forms.CharField(max_length=10, label="your name")
    text = forms.CharField(max_length=10, label="your massage")
    birth_year = forms.DateField(widget=forms.DateTimeInput(attrs={"class": "form-control"}))
    color = forms.ChoiceField(choices=FAVORITE_COLOR_CHOICES)
    numbers = forms.ImageField(widget=forms.NumberInput())

    def clean(self):
        name = self.cleaned_data.get("name")
        text = self.cleaned_data.get("text")
        if name == text:
            raise ValidationError("name and text are same", code="name_text_same")


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
        exclude = ("email",)
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "enter your text",
                "style": "max-width: 300px;"
            }),
            "text": forms.Textarea(attrs={
                "class": "form-control",
            }),
        }