# imports
import google.generativeai as genai  # used for generating tailored resume content with Google's Gemini model
from dotenv import load_dotenv  # library to load environment variables from a .env file
from config import API_KEY
import os  # used to access file extensions and environment variables

from html_utils import tailor_resume_html
from latex import tailor_resume_latex

# from html_utils import *

# Load API key from the environment
load_dotenv()
api_key = os.getenv('API_KEY')

# Configure the Google Generative AI library
genai.configure(api_key=API_KEY)

def tailor_resume(file_path:str, job_description:str, type='html')->None:
    """
    Main function to tailor a resume based on a job description.

    Parameters:
    file_path (str): Path to the original resume file (.docx or .pdf).
    job_description (str): Job description to tailor the resume for.
    output_path (str): Path to save the tailored resume LaTeX file.

    Raises:
    RuntimeError: If no job description is provided or if the file type is unsupported.
    """
    # tailored_resume_html(job_description,output_path)
    if type == 'html':
        output_path = "tailored_resume/tailored_resume.html"
        tailor_resume_html(file_path,job_description,output_path)
    else:
        output_path = "tailored_resume/tailored_resume.tex"
        tailor_resume_latex(file_path,job_description,output_path)
