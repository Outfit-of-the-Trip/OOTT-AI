FROM python:3.9

RUN mkdir -p /app
COPY . /app/
WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app/"
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION "python"

RUN apt-get -qq update && apt-get -y install libgl1-mesa-glx cron
RUN apt-get -y install ./google-chrome-stable_current_amd64.deb

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN cp crawling_cronjob /etc/cron.d/crawling_cronjob
RUN chmod -x /etc/cron.d/crawling_cronjob
RUN crontab /etc/cron.d/crawling_cronjob

ENTRYPOINT ["python3", "server.py"]
EXPOSE 5543