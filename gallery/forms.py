from django import forms
from .models import IrisSample


class IrisSampleForm(forms.ModelForm):
    class Meta:
        model = IrisSample
        fields = ['instance_id', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()
