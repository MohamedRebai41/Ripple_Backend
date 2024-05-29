# Use the official Python 3.12 image as the base
FROM python:3.12-slim


# Update package list and install system dependencies
RUN apt-get update \
  && apt-get -y install gcc make curl 
# Set the working directory
WORKDIR /app

# Copy the rest of the application files
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
