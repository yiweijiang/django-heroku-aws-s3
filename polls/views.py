from django.shortcuts import render
from polls.models import *

def index(request):
    if request.method == 'POST':
        image_file = request.FILES.get('file', False)
        if image_file:
            upload = Image(image=image_file)
            print(upload, image_file)
            upload.save()
        else:
            print('error')
    return render(request, 'index.html')