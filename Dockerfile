FROM python:3.9-alpine

RUN adduser -D server
WORKDIR /server

COPY requirements.txt .
RUN pip3 install -r requirements.txt

USER server

COPY . .

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]