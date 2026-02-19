from django import forms
from .models import Patient

class VCFUploadForm(forms.ModelForm):
    drugs = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'CODEINE, WARFARIN, CLOPIDOGREL, ...',
            'id': 'drug_input'
        }),
        help_text="Comma-separated list of drugs to assess."
    )

    class Meta:
        model = Patient
        fields = ['uploaded_file']
        widgets = {
            'uploaded_file': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'vcf_file',
                'accept': '.vcf'
            })
        }
