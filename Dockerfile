FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
#COPY ./src/requirements.txt /app/
COPY ./src/ /app/
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
RUN pip install gunicorn

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "cybercamp_backoffice.wsgi:application"]

