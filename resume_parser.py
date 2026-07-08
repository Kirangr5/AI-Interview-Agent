import PyPDF2

def extract_resume_text(uploaded_file):

    text = ""

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text