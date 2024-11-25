import fitz  # library to handle PDF files
import docx  # library to handle DOCX files
import os  # used to access file extensions and environment variables
import mimetypes # used to check the resume file type



def get_file_extension(file_path:str)->str:
    """
    Returns the extension of a given file.

    Parameters:
    file_path (str): Path to the file.

    Returns:
    str: File extension (without the dot).
    """
    # Split the file path and get the extension without the dot
    return os.path.splitext(file_path)[1][1:]


# Function to load resume from a pdf file
def load_pdf_resume(file_path: str)->str:
    """
    Loads and returns text content from a PDF resume file.

    Parameters:
    file_path (str): Path to the PDF file.

    Returns:
    str: Text content extracted from the PDF file.
    """
    text = ""
    # Open the PDF file
    with fitz.open(file_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            # Extract text from each page
            page = pdf_document[page_num]
            text += page.get_text()
    return text



# Function to load resume from a Word file
def load_docx_resume(file_path:str)->str:
    """
    Loads and returns text content from a DOCX resume file.

    Parameters:
    file_path (str): Path to the DOCX file.

    Returns:
    str: Text content extracted from the DOCX file.
    """
    doc = docx.Document(file_path)
    resume_text = "\n".join([para.text for para in doc.paragraphs])
    return resume_text