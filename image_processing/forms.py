# image_processing/forms.py

from django import forms

class ImageUploadForm(forms.Form):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), required=True)
    letters = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите буквы слитно, например: АПРУNQ'}), required=False)
    modelSelect = forms.ChoiceField(choices=[('vqfont', 'VQ-Font'), ('mxfont', 'MX-Font')], required=True)




