# Use the official Python image as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port on which the app will run
EXPOSE 5000

# Define environment variables (can be overwritten by Docker run command or docker-compose)
ENV FLASK_APP=your_flask_app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Command to run the application
CMD ["flask", "run"]