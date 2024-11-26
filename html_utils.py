import pdfkit
from latex import read_resume_template
from utils import *
import google.generativeai as genai  # used for generating tailored resume content with Google's Gemini model

def convert_html_to_pdf(html_path: str, pdf_path: str) -> None:
    """
    Converts an HTML file to a PDF using pdfkit.

    Parameters:
    html_path (str): Path to the HTML file.
    pdf_path (str): Path to save the PDF file.
    """
    pdfkit.from_file(html_path, pdf_path, css='resume templates/css template 1.css')

def save_tailored_resume_to_html(tailored_text: str, output_path: str) -> None:
    """
    Saves tailored resume content to an HTML file.

    Parameters:
    tailored_text (str): Content of the tailored resume in HTML format.
    output_path (str): Path to save the tailored resume file.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(tailored_text)

def remove_until_first_newline(s):
    return s.split('\n', 1)[-1]


def tailor_resume_with_gemini_html(resume_text: str, job_description: str, resume_template: str)->str:
    """
    Uses Google's Gemini model to tailor a resume based on a job description.

    Parameters:
    resume_text (str): Original resume content.
    job_description (str): Job description to tailor the resume for.
    resume_template (str): Template to structure the tailored resume.

    Returns:
    str: Tailored resume content in LaTeX format.

    Raises:
    RuntimeError: If the Gemini response contains content in unsupported languages.
    """
    prompt = f"""
    Here is a job description:
    {job_description}

    Here is the current resume:
    {resume_text}
    
    Here is a resume template for you to use:
    {resume_template}

    ##################################################

    Based on the job description, modify the resume to best suit the role by tailoring relevant skills, experiences, and phrasing. 

    - Provide the tailored resume in valid HTML format.
    - Do not include any explanatory text, comments, or additional notes.
    - Ensure the output is fully formatted, as if it were the final version intended for submission.
    - Use appropriate tags for headings, bullet points, and sections.
    - Preserve any existing links from the original resume; do not invent or omit links.
    - Ensure the resume is well-structured, visually appealing, and fits on one page.
    - Provide the tailored resume in plain text format
    """

    # model = genai.GenerativeModel('gemini-1.5-flash')
    # model = genai.GenerativeModel('gemini-1.5-flash-8b')
    model = genai.GenerativeModel('gemini-1.5-pro')


    # sending the prompt to gemini
    response = model.generate_content(prompt)
    print("\n####### Response successfully generated #######\n")
    # Extract the lyx_code from the response
    lyx_code = response.text.strip()
    # lyx_code = " ".join([word for word in lyx_code.split() if word != "'''html"])

    lyx_code = lyx_code.replace("'''html\n", "")
    lyx_code = lyx_code.replace("'''", "")
    # lyx_code = remove_until_first_newline(lyx_code)

    print("########################## GEMINI RESPONSE ##########################\n\n")
    print(lyx_code)
    print("\n\n########################## GEMINI RESPONSE ##########################\n\n")

    return lyx_code


def tailor_resume_html(file_path:str, job_description:str, output_path="Tailored_Resume.html")->None:
    """
    Main function to tailor a resume based on a job description.

    Parameters:
    file_path (str): Path to the original resume file (.docx or .pdf).
    job_description (str): Job description to tailor the resume for.
    output_path (str): Path to save the tailored resume LaTeX file.

    Raises:
    RuntimeError: If no job description is provided or if the file type is unsupported.
    """
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
    resume_template = read_resume_template("resume templates/html template 1.txt")

    # resume_text = load_docx_resume(file_path)
    # tailored_resume = tailor_resume_with_gemini_latex(resume_text, job_description, resume_template)
    tailored_resume = tailor_resume_with_gemini_html(resume_text, job_description, resume_template)

    # Save the tailored resume
    # save_tailored_resume_to_tex(tailored_resume, output_path)
    save_tailored_resume_to_html(tailored_resume, output_path)

    convert_html_to_pdf(output_path, "Tailored_Resume.pdf")

    # compile_latex_file(output_path)

    print(f"Tailored resume saved to Tailored_Resume.pdf")
