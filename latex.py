import subprocess  # used to compile LaTeX files with the `xelatex` command
from utils import *
import google.generativeai as genai  # used for generating tailored resume content with Google's Gemini model


"""
* Function Definitions
"""
# Read resume template file
def read_resume_template(file_path:str)->str:
    """
    Reads and returns the content of a resume template file.

    Parameters:
    file_path (str): Path to the template file.

    Returns:
    str: Content of the resume template.

    Raises:
    FileNotFoundError: If the file does not exist.
    IOError: If an error occurs while reading the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print("Error: File not found.")
    except IOError:
        print("Error: An error occurred while reading the file.")


# Function to save tailored resume to a tex file
def save_tailored_resume_to_tex(tailored_text: str, output_path: str)->None:
    """
    Saves tailored resume content to a specified file path.

    Parameters:
    tailored_text (str): Content of the tailored resume.
    output_path (str): Path to save the tailored resume file.
    """
    with open(output_path, 'w') as f:
      f.write(tailored_text)

# Function to tailor resume using gemini API
def tailor_resume_with_gemini_latex(resume_text: str, job_description: str, resume_template: str)->str:
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

    Based on the job description, modify the resume to best suit the role by tailoring relevant skills, experiences, and phrasing. Ensure that the final content adheres to the following requirements:

    - Provide the modified resume **exclusively in LaTeX code format**, ready for compilation using `xelatex`.
    - Include only English text. Avoid non-English content.
    - Do not include any explanatory text, comments, or additional notes.
    - Ensure the output is fully formatted, as if it were the final version intended for submission.
    - Preserve any existing links from the original resume; do not invent or omit links.
    - Avoid LaTeX syntax issues such as misplaced alignment tabs (`&`) and ensure there are no errors such 
    as "Missing begin document.
    - Aim to fit the resume onto a single page, following the provided template.
    -make sure it fits XeTeX, Version 3.141592653-2.6-0.999996 (TeX Live 2024) (preloaded format=xelatex)
    - DO NOT INCLUDE ANY OTHER SIGNS OR CHARACTERS RATHER THAN THE LYCH CODE

    If these conditions cannot be met, do not attempt to fix them; simply write the number "69" to indicate an error. Otherwise, produce a valid, polished resume.
    """

    # model = genai.GenerativeModel('gemini-1.5-flash')
    # model = genai.GenerativeModel('gemini-1.5-flash-8b')
    model = genai.GenerativeModel('gemini-1.5-pro')


    # sending the prompt to gemini
    response = model.generate_content(prompt)
    print("\n####### Response successfully generated #######\n")
    # Extract the lyx_code from the response
    cleaned_response = response.text.strip()

    # check if we got some bad answer from gemini
    # if lyx_code == "69":
    #     raise RuntimeError("Got different language")
    # return the response
    # lyx_code.replace("''' latex", '')
    # cleaned_response = cleaned_response.replace("&", r"\&")
    cleaned_response = cleaned_response.strip("'''")
    cleaned_response = cleaned_response.strip("latex")

    print("########################## GEMINI RESPONSE ##########################\n\n")
    print(cleaned_response)
    print("\n\n########################## GEMINI RESPONSE ##########################\n\n")

    return cleaned_response



# Function to compile the LaTeX file using xelatex
def compile_latex_file(output_path:str)->str:
    """
    Compiles a LaTeX file into a PDF using the `xelatex` command.

    Parameters:
    output_path (str): Path to the LaTeX (.tex) file.

    Raises:
    RuntimeError: If an error occurs during compilation or if `xelatex` is not found.
    """
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


def tailor_resume_latex(file_path:str, job_description:str, output_path="Tailored_Resume.latex")->None:
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
    resume_template = read_resume_template("resume templates/1.txt")

    # resume_text = load_docx_resume(file_path)
    tailored_resume = tailor_resume_with_gemini_latex(resume_text, job_description, resume_template)

    # Save the tailored resume
    save_tailored_resume_to_tex(tailored_resume, output_path)

    compile_latex_file(output_path)

    print(f"Tailored resume saved to Tailored_Resume.pdf")