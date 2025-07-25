# Use the official lightweight Python image.
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Expose the port Cloud Run expects
EXPOSE 8080

# Run the application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:create_app()"] 