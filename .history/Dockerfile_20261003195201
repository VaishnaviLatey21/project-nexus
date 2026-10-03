FROM python:3.12-slim

WORKDIR /applications

COPY applications/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY applications/ .

EXPOSE 8080

ENV APP_VERSION=dev

CMD ["python", "app.py"]