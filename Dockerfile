FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y && apt-get install -y npm

COPY app ./app

RUN mkdir -p /app/config

EXPOSE 8000

CMD ["python", "-m", "app.main"]