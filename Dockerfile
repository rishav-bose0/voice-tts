# Use an official Python runtime as a parent image
FROM python:3.10.4


RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

#ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8080", "-w", "5", "--timeout", "240", "web.run:app"]
