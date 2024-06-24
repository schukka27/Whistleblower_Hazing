from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['first_name', 'last_name', 'email', 'organization', 'date', 'location', 'description', 'publish', 'anonymous_account']
