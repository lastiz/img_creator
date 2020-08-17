FROM python:3.8-slim

RUN apt-get update \
    && apt-get install -y build-essential

ADD requirements.txt /

RUN pip install -r /requirements.txt

WORKDIR /srv

ADD src/ /srv

CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
