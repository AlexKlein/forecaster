# Use an official Python runtime as a parent image
FROM python:3.7-slim-stretch

# Set the working directory to /app
WORKDIR /app

# Copy the requirements for Python app
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN apt update && apt install -y libpq-dev gcc
RUN pip install --upgrade pip \
 && pip install --trusted-host pypi.python.org -r requirements.txt 

# Copy the current directory contents into the container at /app
COPY . /app

# Run app when the container launches
CMD ["python", "run.py", "start_api", "--host=0.0.0.0", "--port=8080"]