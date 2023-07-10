from django import forms
from .models import Documents

class UploadFileForm(forms.Form):
	title = forms.CharField(max_length=120)
	file = forms.FileField()


class UpFile(forms.ModelForm):

	class Meta:
		model = Documents
		fields = ['documents']