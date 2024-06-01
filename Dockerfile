FROM python:3.12.2-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn project.wsgi:application --bind 0.0.0.0:"${PORT}" --workers 3 --timeout 120

EXPOSE ${PORT}