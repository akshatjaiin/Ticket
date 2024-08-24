FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential  libpq-dev && rm -rf /var/lib/apt/lists/*

# Install pip and dependencies
RUN pip install --upgrade pip
RUN pip install gunicorn 

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Run migrations (this should be done as part of the deployment process, so adjust as needed)
RUN python manage.py migrate --noinput

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Start the Django application
CMD ["gunicorn","MUSEUM_BOT.asgi:application" ,"-k" ,"uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"] 
