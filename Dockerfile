FROM python:3.6

WORKDIR /app

ADD . /app
RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "run.py"]