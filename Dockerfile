FROM python:2.7

MAINTAINER Sergey Cherkesov <go.for.broke1006@gmail.com>

#RUN python --version
RUN apt-get update
RUN apt-get install -y nano curl cron

ENV PYTHONPATH /app/

ADD crontab /var/spool/cron/crontabs/ad-hub-cron
#ADD crontab /etc/cron.d/ad-hub-cron
ADD . /app/

RUN pip install -r /app/requirements.txt

RUN chmod +x /app/docker/run.sh

COPY .env /app/.env
RUN bash -c "source /app/.env"

WORKDIR /app
#CMD tail -f /dev/null
#CMD cron && tail -f /var/log/cron.log
CMD bash /app/docker/run.sh
