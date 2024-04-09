from django.conf.urls.static import static
from django.urls import path

from SpendScan import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/', views.RoomView.as_view()),
    path('upload/', views.image_upload, name='image-upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

