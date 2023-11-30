from django import forms 
from .models import Patient

class RegisterPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['f_name', 'l_name', 'age', 'gender', 'email', 'tel_num', 'comment']