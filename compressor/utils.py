import os

def handle_upload_file(f):
    if(not os.path.exists('compressable_pdfs')):
        os.makedirs('compressable_pdfs')
    
    file_path = os.path.join('compressable_pdfs', f.name)

    with open(file_path, "wb") as file:
        for chunk in f.chunks():
            file.write(chunk)

def read_pdf():
    os.chdir("compressable_pdfs")
    files = os.listdir()
    pdfs = [pdf for pdf in files if pdf.endswith('.pdf')]
    return pdfs[0]