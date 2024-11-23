# Use a lightweight Python image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements to cache dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose Flask port
EXPOSE 5000

# Set Flask environment variables
ENV FLASK_APP=run.py

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]