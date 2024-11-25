from flask import Flask, request, send_file, render_template # Import necessary Flask modules for web app functionalities
import os  # Used for file operations like path handling and directory creation
import cv_tailor as CVT  # Custom module for tailoring resume

# Initialize Flask app
app = Flask(__name__)

def tailor_resume(resume_path, job_description):
    """
    Tailors a resume to a specific job description using the CVT module.

    Parameters:
    resume_path (str): Path to the uploaded resume file.
    job_description (str): Job description text used to tailor the resume.

    Returns:
    str: Path to the tailored resume PDF.
    """
    tailored_resume_path = "tailored_resume/tailored_resume.tex"  # Define path for saving the tailored
    # resume
    CVT.tailor_resume(resume_path, job_description, output_path=tailored_resume_path)
    return "tailored_resume.pdf"

@app.route('/')
def index():
    """
    Renders the home page of the application.

    Returns:
    Template: HTML template for the index page.
    """
    return render_template('index.html')

@app.route('/process_resume', methods=['POST'])
def process_resume():
    """
    Processes the resume and job description submitted by the user to tailor a resume.

    Returns:
    File: The tailored resume PDF for download.
    Error Message: If an error occurs during processing, returns an error message with a 500 status code.
    """

    resume_file = request.files['resume']  # Access the uploaded resume file from the request
    job_description = request.form['job_description']  # Get job description text from the form

    # Define path to save the uploaded resume
    resume_path = os.path.join('uploads', resume_file.filename)
    resume_file.save(resume_path)  # Save the resume file to the defined path

    try:
        # Generate tailored resume and save it to a specified path
        tailored_resume_path = tailor_resume(resume_path, job_description)

        # Serve the tailored resume PDF for download
        return send_file(tailored_resume_path, as_attachment=True, mimetype='application/pdf')
    except RuntimeError as e:
        # If an error occurs, send an error message back to the client
        return f"Error: {str(e)}. Please try reloading the site and retrying.", 500

if __name__ == '__main__':
    # # Create directories for storing uploaded and tailored resume files if they don't exist
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('tailored_resume', exist_ok=True)

    # Run the Flask app in debug mode
    app.run(host='0.0.0.0', port=8080)
    # app.run(debug=True)