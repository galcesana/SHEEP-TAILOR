# Use a Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies including xelatex and fonts
RUN apt-get update && apt-get install -y \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-latex-extra \
    curl \
    && apt-get clean

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that Flask will run on
EXPOSE 8080

# Set environment variables for better Flask behavior in Docker
ENV PYTHONUNBUFFERED=1

# Run the Flask app
CMD ["python", "main.py"]
