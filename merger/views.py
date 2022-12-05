from django.shortcuts import render, HttpResponse, redirect
from PyPDF2 import PdfFileMerger, PdfFileReader


from datetime import date
import time
import os
from pathlib import Path
import shutil


from .forms import UploadPdf
from .utils import handle_upload_file, read_pdf

# Create your views here.

pdfs = []

BASE_DIR = Path(__file__).resolve().parent.parent


def homepage(req):
    return render(req, 'merger/merge.html', {'data': pdfs})

def upload_pdf(req):

    if(req.method == "POST"):
        form = UploadPdf(req.POST, req.FILES)
        if(form.is_valid()):
            handle_upload_file(req.FILES['pdf'])
            pdfs.append(form.cleaned_data['pdf'])
            return redirect("/merger")
    else:
        return HttpResponse("501 Server Issue :(")


def merge_pdf(req):

    merger = PdfFileMerger()
    pdf_data = read_pdf()

    for pdf in pdf_data:
        merger.append(PdfFileReader(open(pdf, 'rb')))

    # getting current date and time
    today = date.today()
    current_date = today.strftime("%d%m%Y")
    current_time_seconds = time.time()

    # creating a new directory for merged pdfs
    os.chdir('../')
    os.mkdir("final_pdf") if(not os.path.exists('final_pdf')) else ''
    os.chdir('final_pdf/')

    # naming the final pdf
    merger.write(f"{current_time_seconds}_{current_date}_merged.pdf")


    return HttpResponse("<a href='/merger/download-pdf'>download</a>")
    


def download_pdf(req):

    files = os.listdir()

    pdf = None
    
    with open(files[0], "rb") as f:
        pdf = f.read()
    
    # download the file with sending the response
    response = HttpResponse(pdf, content_type="application/vnd.pdf")
    response['Content-Disposition'] = f"attachment; filename={files[0]}"

    #  changing the directory
    os.chdir("../")
    
    # deleting the pdf containing folders
    shutil.rmtree("final_pdf", ignore_errors=True) if(os.path.exists("final_pdf")) else ''
    shutil.rmtree("raw_pdfs", ignore_errors=True) if(os.path.exists("raw_pdfs")) else ''

    return response