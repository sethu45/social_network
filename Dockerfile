FROM python:3.11.4

ENV PYTHONUNBUFFERED 1

WORKDIR /app/social_network

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000