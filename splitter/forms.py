from django import forms


class UploadPdf(forms.Form):
    pdf = forms.FileField()