FROM python:3.10

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

# Apply database migrations and collect static files
# RUN python manage.py makemigrations
# RUN python manage.py migrate
# RUN python manage.py collectstatic --noinput

# Expose the Django port
EXPOSE 8000

# Run the Django application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project_name.wsgi:application"]
