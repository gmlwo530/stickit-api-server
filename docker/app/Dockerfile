FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ARG INSTALL_DEV=false

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.7

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Install Poetry
# RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
#     cd /usr/local/bin && \
#     ln -s /opt/poetry/bin/poetry && \
#     poetry config virtualenvs.create false

RUN /usr/local/bin/python -m pip install --upgrade pip && \
    /usr/local/bin/python -m pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.create false && \
    poetry install $(test "$INSTALL_DEV" == "false" && echo "--no-dev") --no-root --no-interaction --no-ansi

# Allow installing dev dependencies to run tests

COPY ./app /app
# ENV PYTHONPATH=/app

WORKDIR /

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]