FROM python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade pip
COPY req.txt /app/

RUN pip install -r req.txt

COPY . /app/