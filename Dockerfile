FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/usr/src/app \
    USER=django

# Create custom user for security
RUN useradd --create-home $USER

# Create directory structure
WORKDIR $APP_HOME

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories and set permissions
RUN mkdir  -p $APP_HOME/.db \
    && chown -R $USER:$USER $APP_HOME

# Copy project files
COPY --chown=$USER:$USER app $APP_HOME/app/

# Switch to non-root user
USER $USER

# Set the working directory to where manage.py is located
WORKDIR $APP_HOME/app

ENV STAGE=dev-local

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]