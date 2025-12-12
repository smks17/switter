FROM python:3.12
RUN mkdir /app
WORKDIR /app
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

COPY entrypoint.sh /tmp/entrypoint.sh
RUN cat /tmp/entrypoint.sh | tr -d '\r' > /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Run Django’s server
CMD ["/bin/sh", "-c", "python manage.py migrate --noinput && gunicorn switter.wsgi:application --bind ${DJANGO_HOST}:${DJANGO_PORT} --workers ${DJANGO_NUM_WORKERS} --timeout 120 --log-level ${DJANGO_LOG_LEVEL}"]