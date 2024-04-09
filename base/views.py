from urllib.request import urlopen
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile

from base.models import Image

from django.shortcuts import render
from django.http import HttpResponse
# from django.core.files.storage import FileSystemStorage
# from corona.analyzer import main
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files.storage import default_storage
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RoomSerializer
from .models import Room


# Create your views here.
def home(request):
    return HttpResponse('Welcome to home')


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

def image_upload(request):
    if request.method == 'POST':
        image_path = request.POST["src"]
        print(image_path)

        image = NamedTemporaryFile()
        urlopen(image_path).read()
        image.write(urlopen(image_path).read())
        image.flush()
        image = File(image)
        name = str(image.name).split('\\')[-1]
        name += '.jpg'  # store image in jpeg format
        image.name = name
        # with open('image.txt', 'w+') as file:
        #     file.write(str(name))
        # default_storage.save('C:/Users/User/PycharmProjects/SpendScan/media/imga.jpg', ContentFile(urlopen(image_path).read()))
        # return HttpResponse('Done!')

        if image is not None:
            obj = Image.objects.create(username='yes', image=image)  # create a object of receipts_training type defined in your model
            obj.save()
        return HttpResponse('Done!')
    return render(request, 'base/index.html')