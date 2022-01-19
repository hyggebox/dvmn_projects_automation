from django import forms

from .models import TimeSlot


class ChooseTimeForm(forms.Form):
    best_time_slots = forms.ModelMultipleChoiceField(
        label='Наиболее удобное время',
        queryset=TimeSlot.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    ok_time_slots = forms.ModelMultipleChoiceField(
        label='Менее удобное время, но возможное',
        queryset=TimeSlot.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )


