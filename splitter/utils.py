import os

def handle_upload_file(f):
    if(not os.path.exists('split_pdf_folder')):
        os.makedirs('split_pdf_folder')
    
    file_path = os.path.join('split_pdf_folder', f.name)

    with open(file_path, "wb") as file:
        for chunk in f.chunks():
            file.write(chunk)

def read_pdf():
    os.chdir("split_pdf_folder")
    files = os.listdir()
    pdfs = [pdf for pdf in files if pdf.endswith('.pdf')]
    return pdfs