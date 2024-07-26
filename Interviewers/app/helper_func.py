import PyPDF2
import docx


def extract_text(file_path):
    if str(file_path).endswith(".pdf"):
       return extract_text_from_pdf(str(file_path))
    elif str(file_path).endswith(".docx"):
       return extract_text_from_docx(str(file_path))
    elif str(file_path).endswith(".txt"):
       return extract_text_from_txt(str(file_path))
    else:
        return "Please upload only .docx,.pdf,.txt"

def extract_text_from_pdf(file_path):
    text=""
    with open(file_path,'rb') as file:
      reader = PyPDF2.PdfReader(file)
      for pages in reader.pages:
         text+=pages.extract_text()
    return text

def extract_text_from_docx(file_path):
   doc = docx.Document(file_path)
   text = ""
   for para in doc.paragraphs:
      text+=para.text
   return text
    


def extract_text_from_txt(file_path):
   # Step 1: Open the file in read mode with UTF-8 encoding
    with open(file_path, "r", encoding="utf-8") as file:
    # Step 2: Read the contents of the file
        text = file.read()
    return text

   




    