from django.urls import path, include
from .views import *

urlpatterns = [
    path('', homepage, name="homepage"),
    path('pdf_options', upload_pdf, name="pdf_options"),
    path('split_pdf', split_pdf, name="split_pdf"),
]