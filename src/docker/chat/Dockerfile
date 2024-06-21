# Base off the official python image
# Define a common stage for dev and prod images called base
FROM --platform=linux/amd64 python:3 as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a user to avoid running containers as root in production
RUN addgroup --system web \
    && adduser --system --ingroup web web

# Install os-level dependencies (as root)
RUN apt-get update && apt-get install -y -q --no-install-recommends \
    build-essential \
    curl \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Create the necessary directories for the 'web' user and set permissions
RUN mkdir -p /home/web/.local/bin \
    && chown -R web:web /home/web

# Switch to the non-root user
USER web

# Set the HOME environment variable to the home directory of the 'web' user
ENV HOME=/home/web

# Verify the directory structure and permissions
RUN ls -alh /home/web

# Switch back to root user to install Poetry and dependencies
USER root

# Install Poetry for python dependency management
# https://python-poetry.org/docs/master/#installation
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the PATH to include the Poetry bin directory
ENV PATH="/home/web/.local/bin:$PATH"

# Switch to the web user and set the working directory
USER web
WORKDIR /home/web/code/

# Copy the python dependencies list for poetry
COPY --chown=web:web poetry.lock pyproject.toml ./

# Switch to root user to install Python packages globally
USER root

# Install Python packages globally
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction

# Switch back to the non-root user
USER web

# Copy entrypoint script which waits for the db to be ready
COPY --chown=web:web ./docker/chat/entrypoint.sh /usr/local/bin/entrypoint.sh

# Switch to root user to grant execution permissions
USER root
RUN chmod +x /usr/local/bin/entrypoint.sh
USER web

# Set entrypoint
ENTRYPOINT ["entrypoint.sh"]

# Define an image for local development. Inherits common packages from the base stage.
FROM base as dev

# Install python packages at system level, including development dependencies
USER root
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction
USER web
COPY --chown=web:web ./docker/chat/start-dev-server.sh /usr/local/bin/start-dev-server.sh
USER root
RUN chmod +x /usr/local/bin/start-dev-server.sh
USER web
# The development server starts by default when the container starts
CMD ["start-dev-server.sh"]


# Define an image for production. Inherits common packages from the base stage.
FROM base as prod
# Install python packages at system level, without development dependencies
RUN /bin/true\
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-dev \
    && rm -rf /home/web/.cache/pypoetry
# Copy the script that starts the production application server (gunicorn)
COPY --chown=web:web ./docker/chat/start-prod-server.sh /usr/local/bin/start-prod-server.sh
USER root
RUN chmod +x /usr/local/bin/start-prod-server.sh
USER web
# Copy the source code of our django app to the working directoy
COPY --chown=web:web . ./
# The production server starts by default when the container starts
CMD ["start-prod-server.sh"]