from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Note, HomeWork, Todo

class NoteForm(forms.ModelForm):
  class Meta:
    model = Note 
    fields = ("title", "description")
    
    widgets = {
      "title": forms.TextInput(
        attrs={
          "placeholder": "Note title..",
          "class": "form-control",
        }),
      "description": forms.Textarea(
        attrs={
          "placeholder": "Description..",
          "row": 6,
          "class": "form-control",
        }),
    }


class DateInput(forms.DateInput):
  input_type = "date"


class HomeWorkForm(forms.ModelForm):
  class Meta:
    model = HomeWork 
    fields = ("subject", "title", "description", "due")
    
    widgets = {
      "subject": forms.TextInput(
        attrs={
          "placeholder": "Subject..",
          "class": "form-control",
        }),
      "title": forms.TextInput(
        attrs={
          "placeholder": "Homework title..",
          "class": "form-control",
        }),
      "due": DateInput(attrs={
        "class": "form-control",
        "placeholder": "Due date..",
      }),
      "description": forms.Textarea(
        attrs={
          "placeholder": "Description..",
          "row": 6,
          "class": "form-control",
        }),
    }


class TodoForm(forms.ModelForm):
  class Meta:
    model = Todo 
    fields = ("title",)
    
    widgets = {
      "title": forms.TextInput(
        attrs={
          "placeholder": "Enter task title..",
          "class": "form-control",
        }),
    }


class ConversionForm(forms.Form):
  CHOICES = [("length", "Length"), ("mass", "Mass")]
  measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)


class ConversionLengthForm(forms.Form):
  CHOICES = [("yard", "Yard"), ("foot", "Foot")]
  input = forms.CharField(required=False, label=False, widget=forms.TextInput(
    attrs={"type": "number", "placeholder": "Enter the number"}
  ))
  measure1 = forms.CharField(label="", widget=forms.Select(choices=CHOICES))
  measure2 = forms.CharField(label="", widget=forms.Select(choices=CHOICES))


class ConversionMassForm(forms.Form):
  CHOICES = [("pound", "Pound"), ("kilogram", "Kilogram")]
  input = forms.CharField(required=False, label=False, widget=forms.TextInput(
    attrs={"type": "number", "placeholder": "Enter the number"}))
  measure1 = forms.CharField(label="", widget=forms.Select(choices=CHOICES))
  measure2 = forms.CharField(label="", widget=forms.Select(choices=CHOICES))


class UserRegistrationForm(UserCreationForm):
  class Meta:
    model = User 
    fields = ("username", "password1", "password2")
