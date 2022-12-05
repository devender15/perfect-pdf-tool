from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name="homepage"),
    path('upload/', upload_pdf, name="upload"),
    path('merge-pdf/', merge_pdf, name="merge-pdf"),
    path('download-pdf/', download_pdf, name="download-pdf"),
]