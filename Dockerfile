FROM python:3.9-alpine

RUN adduser -D server
WORKDIR /server

# Copy requirements first as to not disturb cache for other changes.
COPY requirements.txt .
RUN pip3 install -r requirements.txt

USER server

# Finally, copy the entire source.
COPY . .

ENTRYPOINT ["python3", "app.py"]
