FROM python:3.10.4

WORKDIR /home/

RUN echo "testing13333"

RUN git clone https://github.com/wondora/gshs2.git

WORKDIR /home/gshs2/

RUN pip install -r requirements.txt

RUN pip install mysqlclient

EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --noinput --settings=gshs2.settings && python manage.py migrate --settings=gshs2.settings && gunicorn gshs2.wsgi --env DJANGO_SETTINGS_MODULE=gshs2.settings --bind 0.0.0.0:8000"]