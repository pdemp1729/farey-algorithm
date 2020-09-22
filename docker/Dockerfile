FROM python:3.7-slim

WORKDIR /app

ARG APP_USER="bob"
ARG APP_UID="1000"

# Add /app to the python path. This ensures we can import modules correctly
ENV PYTHONPATH="$PYTHONPATH:/app"
# Set the locale
ENV LANG=C.UTF-8

# Upgrade pip
RUN pip3 install --upgrade pip

# Copy over the requirements file
COPY docker/requirements.txt /tmp/requirements.txt

# Install additional requirements for the package
RUN pip3 install --trusted-host pypi.python.org -r /tmp/requirements.txt && \
    apt-get autoremove -y

COPY . /app

# Create a non-root user
RUN useradd -u $APP_UID $APP_USER

# Switch to a non-root user
USER $APP_USER
