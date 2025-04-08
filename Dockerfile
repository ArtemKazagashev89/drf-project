FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SECRET_KEY="django-insecure-2o9yfo*wrtfntkwzlh28+octw5$4hbsuk@=b(84do*pf(w@7bm"
ENV CELERY_BROKER_URL='redis://localhost:6379/0'
ENV CELERY_BACKEND='redis://localhost:6379/0'

RUN mkdir -p /app/media

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

