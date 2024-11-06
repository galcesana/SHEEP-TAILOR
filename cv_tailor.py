# imports
import mimetypes # used to check the resume file type
import google.generativeai as genai
import fitz  # handle pdf
import docx  # handle docx
import os  # used to get the file extension
import subprocess
from dotenv import load_dotenv

# loading the api key from my eniourment
load_dotenv()
api_key = os.getenv('API_KEY')
API_KEY = 'AIzaSyBB093d-_sTNO-eaIRvBlzK8RTSOae6-mk'

# configure the Google Generative AI library.
genai.configure(api_key=API_KEY)

"""
*functions*

*tailoring the resume using gemini*
"""
# Read resume template file
def read_resume_template(file_path:str)->str:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print("Error: File not found.")
    except IOError:
        print("Error: An error occurred while reading the file.")

# Function to load resume from a Word file
def load_docx_resume(file_path:str)->str:
    doc = docx.Document(file_path)
    resume_text = "\n".join([para.text for para in doc.paragraphs])
    return resume_text

# Function to load resume from a pdf file
def load_pdf_resume(file_path: str)->str:
    text = ""
    # Open the PDF file
    with fitz.open(file_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            # Extract text from each page
            page = pdf_document[page_num]
            text += page.get_text()
    return text

# Function to save tailored resume to a tex file
def save_tailored_resume(tailored_text: str, output_path: str)->None:
    with open(output_path, 'w') as f:
      f.write(tailored_text)

# Function to tailor resume using gemini API
def tailor_resume_with_gemini(resume_text: str, job_description: str, resume_template: str)->str:
    # Construct the prompt for the gemini API
    prompt = f"""
    Here is a job description:
    {job_description}

    Here is the current resume:
    {resume_text}
    
    Here is a resume template for you to use:
    {resume_template}
    
    
    ##################################################
    
    Based on the job description, please modify the resume to best suit the role by enhancing relevant skills, experiences, and phrasing.
    
    In your response, provide only the modified resume content in LaTeX code format, ready to be compiled 
    With no additional comments or explanatory text. !! The output should appear as if it is the final 
    version intended directly for submission !! if the original resume is missing links do not 
    include them in the modified version, also if it has other links you need to include them.
    Write your response only in English.
    Important - make sure xelatex can compile it! if your text contains other languages than English only 
    Print the number 69 and nothing else.""" # Write it in a way xelatex can compile it and only use Roboto font.
    # setting the gemini model     Try to make it fit 1 page.
    model = genai.GenerativeModel('gemini-1.5-flash')
    # sending the prompt to gemini
    response = model.generate_content(prompt)
    print("\n####### Response successfully generated #######\n")
    # Extract the lyx_code from the response
    lyx_code = response.text.strip()
    print("########################## GEMINI RESPONSE ##########################\n\n")
    print(lyx_code)
    print("\n\n########################## GEMINI RESPONSE ##########################\n\n")
    # check if we got some bad answer from gemini
    if lyx_code == "69":
        raise RuntimeError("Got different language")
    # return the response
    return lyx_code


def get_file_extension(file_path:str)->str:
    # Split the file path and get the extension without the dot
    return os.path.splitext(file_path)[1][1:]

# Function to compile the LaTeX file using xelatex
def compile_latex_file(output_path:str)->str:
    # Get the directory of the .tex file to set as the working directory
    working_directory = os.path.dirname(output_path)
    try:
        # Run the xelatex command
        print(output_path)
        subprocess.run(
            ['xelatex', output_path],
            check=True
        )
        print("PDF compiled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while compiling the PDF: {e}")
        raise RuntimeError("An error occurred during the LaTeX compilation.")
    except FileNotFoundError:
        print("Error: 'xelatex' was not found. Ensure it is installed and in your PATH.")
        raise RuntimeError("The 'xelatex' command was not found. Please check your installation.")

# Main function to tailor resume based on job description
def tailor_resume(file_path:str, job_description:str, output_path="Tailored_Resume.tex")->None:
    # check if we got a job description
    if job_description == "":
        raise RuntimeError("Empty description.")
    input_extension = get_file_extension(file_path)
    if input_extension == 'docx':  # handle Word files
        resume_text = load_docx_resume(file_path)
    elif input_extension == 'pdf':  # handle PDF files
        resume_text = load_pdf_resume(file_path)
    else:
        print("Unsupported file type. Only .docx files are supported.")
        return
    print("\n####### Resume successfully loaded #######\n")
    print(resume_text)
    print("\n####### Resume successfully loaded #######\n")

    # loading the resume template
    resume_template = read_resume_template("resume templates/1.txt")

    # resume_text = load_docx_resume(file_path)
    tailored_resume = tailor_resume_with_gemini(resume_text, job_description, resume_template)

    # Save the tailored resume
    save_tailored_resume(tailored_resume, output_path)

    compile_latex_file(output_path)

    print(f"Tailored resume saved to {output_path}")