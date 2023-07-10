from django.db import models

# Create your models here.
class Documents(models.Model):
	name = models.CharField(max_length=120, blank=True)
	documents = models.FileField(upload_to="static/documents")
	uploaded_at =  models.DateTimeField(auto_now_add=True)