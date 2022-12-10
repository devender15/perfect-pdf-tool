from django.urls import path, include
from .views import *

urlpatterns = [
    path('', homepage, name="homepage"),
    path('upload_pdf', upload_pdf, name="upload_pdf"),
    path('compress_pdf', compress_pdf, name="compress_pdf"),
]