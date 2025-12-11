FROM python:3.9-slim

# Set working directory inside container
WORKDIR /application

# Copy main Python script
COPY app.py /application/

# Ensure database directory exists
RUN mkdir -p /storage/db

# Default command for running the script
CMD ["python", "app.py"]
