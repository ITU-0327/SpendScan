from django.shortcuts import render

# Create your views here.

# goes to frontend/templates/frontend/index.html
# then react start rendering
# finally returns the HTML
def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')

