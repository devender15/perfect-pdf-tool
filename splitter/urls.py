from django.urls import path, include
from .views import *

urlpatterns = [
    path('', split_pdf, name="merge"),
]