FROM python:3.12-slim-bookworm

#Set working directory inside the container
WORKDIR /app
ENV DOCKER=true

#Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    chromium \
    chromium-driver \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#Copy requirements first
COPY requirements.txt .

#Install Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Copy all projects
COPY . .

#SET Chrome to run headless inside container
ENV PYTHONPATH=/app

#Run pytest when container starts
CMD ["pytest", "tests/", "-v", "--html=reports/report.html", "--self-contained-html"]


