FROM python:3.7.4-alpine3.10

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "career_track.wsgi:application"]
