FROM python:3.8-alpine

RUN mkdir -p /app
COPY . /app/
WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app/"
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION "python"

RUN apt-get -y update && apt-get install -y libzbar-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]