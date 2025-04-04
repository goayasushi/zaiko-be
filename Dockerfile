ARG BASE_IMAGE=python:3.12

FROM ${BASE_IMAGE}

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]