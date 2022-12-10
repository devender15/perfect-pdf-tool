from django.shortcuts import render, HttpResponse

import PyPDF2, os, shutil

from .utils import handle_upload_file, read_pdf
from splitter.forms import UploadPdf

# Create your views here.
def homepage(req):
    return render(req, 'compressor/page.html')

def upload_pdf(req):
    shutil.rmtree("compressable_pdfs") if(os.path.exists("compressable_pdfs")) else ""
    if(req.method == 'POST'):
        form = UploadPdf(req.POST, req.FILES)
        if(form.is_valid()):
            handle_upload_file(req.FILES['pdf'])
            pdf = form.cleaned_data['pdf']
            context = {"pdf": pdf}
            return render(req, 'compressor/options.html', context)
    else:
        return HttpResponse("501 Server Issue :(")    

def compress_pdf(req):
    pdf_file = read_pdf()

    downloadable_file = None

    # Open the PDF file for reading
    with open(pdf_file, "rb") as input_file:
        # Create a PDF reader object
        reader = PyPDF2.PdfFileReader(input_file)

        # Create a PDF writer object
        writer = PyPDF2.PdfFileWriter()

        # Loop through all the pages in the PDF
        for page_num in range(reader.getNumPages()):
            # Get the current page
            page = reader.getPage(page_num)

            # Compress the page using the default quality
            page.compressContentStreams()

            # Add the page to the PDF writer
            writer.addPage(page)

        # Open the output PDF file for writing
        with open("../output.pdf", "wb") as output_file:
            # Write the PDF to the file
            writer.write(output_file)

        with open("../output.pdf", "rb") as f:
            downloadable_file = f.read()
    
    os.chdir("../")
    shutil.rmtree("compressable_pdfs", ignore_errors=True)

    response = HttpResponse(downloadable_file, content_type="application/vnd.pdf")
    response['Content-Disposition'] = "attachment; filename=output.pdf"
        
    return response