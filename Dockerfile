FROM python:3.12
RUN mkdir /app
WORKDIR /app
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Build
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Run Django’s server
CMD ["/app/entrypoint.sh"]
