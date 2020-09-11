FROM python:3.7

COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app
COPY ./mysite /app/

EXPOSE 80
CMD python manage.py runserver 0:80
