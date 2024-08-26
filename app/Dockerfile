FROM python:3.8-slim

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python","app.py"]
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]