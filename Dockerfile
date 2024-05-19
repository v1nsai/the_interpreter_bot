# Use the official Python Alpine image as the base
FROM python:3.9-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the main.py and requirements.txt files to the working directory
COPY main.py requirements.txt ./

# Install the Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the main.py script when the container starts
CMD ["python", "main.py"]