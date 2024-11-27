FROM python:3.12-slim

WORKDIR /app

#move back the 'Dockerfile' or change to '..'  
COPY . /app 

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y cron

COPY cron /etc/cron.d/dailycron

RUN chmod 0644 /etc/cron.d/dailycron

RUN crontab /etc/cron.d/dailycron

RUN touch /var/log/cron.log

EXPOSE 8000

CMD ["sh", "-c", "cron && python roshan/manage.py migrate && python roshan/manage.py runserver 0.0.0.0:8000"]
