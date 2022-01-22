from django import forms

from .models import TimeSlot

class PMForm(forms.ModelForm):
    """
    My attributes
    """
    def custom_method(self):
        print("Hello, World!")

class ChooseTimeForm(forms.Form):
    best_time_slots = forms.ModelMultipleChoiceField(
        label='Наиболее удобное время (*время московское)',
        queryset=TimeSlot.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    ok_time_slots = forms.ModelMultipleChoiceField(
        label='Менее удобное время, но возможное (*время московское)',
        queryset=TimeSlot.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


