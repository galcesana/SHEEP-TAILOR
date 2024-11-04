from flask import Flask, request, send_file, render_template
import os
import cv_tailor as CVT

app = Flask(__name__)

# Function to tailor resume (placeholder for your code)
def tailor_resume(resume_path, job_description):
    tailored_resume_path = "tailored_resume/tailored_resume.tex"  # path to save the tailored resume
    CVT.tailor_resume(resume_path, job_description, output_path=tailored_resume_path)
    return "tailored_resume.pdf"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_resume', methods=['POST'])
def process_resume():
    resume_file = request.files['resume']
    job_description = request.form['job_description']

    # Save the uploaded resume file
    resume_path = os.path.join('uploads', resume_file.filename)
    resume_file.save(resume_path)

    try:
        # Generate tailored resume
        tailored_resume_path = tailor_resume(resume_path, job_description)

        # Serve the tailored resume for download
        return send_file(tailored_resume_path, as_attachment=True, mimetype='application/pdf')
    except RuntimeError as e:
        # Return an error message to the client
        return f"Error: {str(e)}. Please try reloading the site and retrying.", 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('tailored_resume', exist_ok=True)
    app.run(debug=True)
