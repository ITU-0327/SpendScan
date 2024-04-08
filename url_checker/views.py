from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def check_url(request):
    try:
        url_status = urllib.request.urlopen(request.body.decode("utf-8") ).getcode()
    except:
        return HttpResponse(":( Url is Not Working")
    if (url_status == 200):
        return HttpResponse("Yey! URL is Working")
    return HttpResponse(":( Url is Not Working")