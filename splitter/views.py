from django.shortcuts import render, HttpResponse

from PyPDF2 import PdfFileWriter, PdfFileReader
import os
from datetime import date
import time
import shutil

from .forms import UploadPdf
from .utils import handle_upload_file


def homepage(req):
    return render(req, 'splitter/split.html', {'data': 'data'})

def upload_pdf(req):

    # deleting the split_pdf_folder to save new file
    shutil.rmtree("split_pdf_folder") if (os.path.exists("split_pdf_folder")) else ""

    if(req.method == "POST"):
        form = UploadPdf(req.POST, req.FILES)
        if(form.is_valid()):
            handle_upload_file(req.FILES['pdf'])
            pdf = form.cleaned_data['pdf']
            context = {"pdf": pdf}
            return render(req, 'splitter/options.html', context)
    else:
        return HttpResponse("501 Server Issue :(")    

def split_pdf(req):

    pdf_folder = os.listdir("split_pdf_folder/")
    pdf_file = PdfFileReader(open(f"split_pdf_folder/{pdf_folder[0]}", "rb"))
    total_pages_pdf = pdf_file.numPages

    # getting current date and time
    today = date.today()
    current_date = today.strftime("%d%m%Y")
    current_time_seconds = time.time()

    if(req.method == "POST"):
        no_of_pages = req.POST.get('range')

        no_of_pages_arr = [i for i in range(total_pages_pdf)]

        composite_list = [no_of_pages_arr[x:x+int(no_of_pages)] for x in range(0, len(no_of_pages_arr), int(no_of_pages))]

        # creating a new directory and saving these splitted pdfs in that directory
        os.mkdir("splitted_pdfs")
        os.chdir("splitted_pdfs/")

        # creating new pdfs
        for i in composite_list:
            output = PdfFileWriter()
            for j in i:
                output.addPage(pdf_file.getPage(j))
            
            with open(f"{current_time_seconds}_{current_date}{i}-split.pdf", "wb") as output_stream:
                output.write(output_stream)

        os.chdir("../")
        shutil.make_archive("split_pdfs", 'zip', "splitted_pdfs")

        # deleting the temporary directory
        shutil.rmtree("splitted_pdfs", ignore_errors=True)

    
    # downloading the zipped file
    zipped_file = None

    with open("split_pdfs.zip", "rb") as f:
        zipped_file = f.read()
    
    # download the file with sending the response
    response = HttpResponse(zipped_file, content_type="application/vnd.zip")
    response['Content-Disposition'] = "attachment; filename=split_pdfs.zip"
        
    return response