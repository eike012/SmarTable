FROM python:3.11

WORKDIR /app

# install required packages
RUN apt-get update && apt-get install -y vim tesseract-ocr tesseract-ocr-por aspell aspell-pt-br

# copy images that will be read by the ocr
COPY . /app

COPY requirements.txt /app
RUN pip install --trusted-host pypi.python.org --no-cache -r requirements.txt
