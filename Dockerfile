FROM python:3.8

WORKDIR /app

# Добавляем установку Flask и Flask-SQLAlchemy с уточненными версиями
RUN pip install Flask==2.0.1 Flask-SQLAlchemy==2.5.1 Flask-Migrate==3.1.0 Werkzeug==2.0.1 SQLAlchemy==1.4.23

COPY . .

CMD ["python", "app.py"]