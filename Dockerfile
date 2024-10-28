# Use an official Python runtime as the base image
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Install dependencies
RUN pip install discord-py-interactions

# Set the command to run the application
CMD python main.py