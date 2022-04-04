FROM python
ENV PYTHONUNBUFFERED=1
RUN mkdir -p /usr/src/app/static
RUN mkdir -p /usr/src/app/media
WORKDIR /usr/src/app/backend
COPY req.txt .
RUN pip install -r req.txt
COPY . .
RUN python manage.py collectstatic --noinput