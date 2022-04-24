#Download base image python 3.7
FROM python:3.7

# LABEL about the custom image
LABEL maintainer="robert@brutuswolf.com"
LABEL version="0.1"
LABEL description="This is custom Docker image for the KrakenFlex interview test"

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

# Update Ubuntu Software repository
RUN apt update

# Set working directory
WORKDIR /app


RUN pip install --upgrade pip

# Copy requirments and install
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy files
COPY . .


#Execute 
# run the command
CMD ["python", "Code/app_run.py"]
