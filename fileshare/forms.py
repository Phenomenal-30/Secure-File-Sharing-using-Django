# fileshare/forms.py
from django import forms
from .models import SharedFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = SharedFile
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith(('.docx', '.pptx', '.xlsx')):
            raise forms.ValidationError("Only .docx, .pptx, .xlsx files allowed")
        return file
