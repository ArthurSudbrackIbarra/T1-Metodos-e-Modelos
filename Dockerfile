# Using the official Python 3.10.11 slim image (Debian).
FROM python:3.10.11-slim

# Arguments for the build.
#
# ENVIRONMENT: development, production.
# Default: development.
#
# MONGODB_HOST: MongoDB connection string.
ARG ENVIRONMENT="development"

# Environment variables.
ENV ENVIRONMENT=${ENVIRONMENT} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.4.1

# Set the working directory.
WORKDIR /app

# Install Java 11 (Needed to use Tabula-Py).
RUN apt update && apt install -y -f openjdk-11-jre-headless

# Install Poetry.
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer.
COPY poetry.lock pyproject.toml /app/

# Project initialization.
RUN poetry config virtualenvs.create false \
    && poetry install $(test "$ENVIRONMENT" == production && echo "--no-dev") --no-interaction --no-ansi

# Copy the rest of the project.
COPY . /app/

# Copy SSL certificates.
COPY ./certs /etc/ssl

# Expose the port.
EXPOSE 443

# Run the application.
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-certfile", "/etc/ssl/certificate.crt", "--ssl-keyfile", "/etc/ssl/private.key"]
