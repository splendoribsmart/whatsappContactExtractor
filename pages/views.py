from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm, UpFile
from .models import Documents
# from .extractor import handle_uploaded_file

from bs4 import BeautifulSoup as bs
import os


from django.conf.urls.static import static
from django.templatetags.static import static



NEW = []


# Create your views here.

def home_view(request):
	return render(request, 'home.html', {})

def extract_view(request):
	if request.method == "POST":
		form = UpFile(request.POST, request.FILES) # UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()

			myid = form.instance.id
			# print("Object ID: ", myid)
			request.session['new_id'] = myid

			obj = Documents.objects.get(id = myid)

			csv_file_name = f"ZootyGrow{myid}.csv"

			obj.name = csv_file_name

			obj.save()

			html = open(obj.documents.name, encoding="utf8")
			soup = bs(html, 'lxml')
			sp1 = soup.find('span', class_="ggj6brxn gfz4du6o r7fjleex lhj4utae le5p0ye3 _11JPr selectable-text copyable-text")
			
			# Finding the span that contains group contact with class
			title = sp1.get('title')
			title = title.split(',')

			# Sorting cleaning out contacts; selecting only those that starts with +234 which is the Nigerian country code
			cont_list = [] 
			for i in title: 
				i = i.replace(" ", "") 
				if i.startswith("+234"): 
					cont_list.append(i) 

			# Formating list of contacts and writing to .txt 
			txt_file_name = f"ZootyGrow{myid}.txt"
			file = open("static/documents/ext/"+txt_file_name, "w")
			count = 0 
			for x in cont_list: 
				count += 1 
				line =  f"{x[4:]},ZG{count},234\n" 
				file.write(line) 

			file.close()

			# try and except to remove if the is file with thesame name from last operation
			os.rename("static/documents/ext/"+txt_file_name, "static/documents/ext/"+csv_file_name)


			 # Rename .txt file to .csv file

			print("Extraction Successful!!!\n\nYour .csv file is ready") # Sucessful message

			# handle_uploaded_file(request.FILES["file"])
			return HttpResponseRedirect("/success/")
	else:
		form = UpFile()
	return render(request, 'extract.html', {"form": form})

def sender_view(request):
	return render(request, 'sender.html', {})

def success_view(request):
	a = request.session['new_id']
	print(a)
	obj = Documents.objects.get(id = a)
	name = obj.name
 	
	url = static('documents/ext/'+ str(name))
	print(url)

	context = {"obj" : obj, "url" : url} 
	return render(request, 'successful.html', context)