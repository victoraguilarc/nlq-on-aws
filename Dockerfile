FROM python:3.12-slim

LABEL name="nlq-genai" \
    version="1.0.0-oai"


ENV PIP_DEFAULT_TIMEOUT=100 \
    # allow statements and log messages to immediately appear
    PYTHONUNBUFFERED=1 \
    # disable a pip version check to reduce run-time & log-spam
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # cache is useless in docker image, so disable to reduce image size
    PIP_NO_CACHE_DIR=1

ENV POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=false

RUN set -ex \
    # create a non-root user
    && groupadd --system --gid 1001 appgroup \
    && useradd --system --uid 1001 --gid 1001 --create-home appuser \
    # upgrade the package index and install security upgrades
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install gcc g++ git make iputils-ping -y \
    # clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/appuser/

COPY pyproject.toml /home/appuser/

RUN pip install --upgrade pip
RUN pip install setuptools
RUN pip install "poetry==$POETRY_VERSION"

RUN poetry config --local installer.no-binary psycopg2
RUN poetry install --no-interaction --no-ansi --with dev

# copy required files to image
COPY --chown=appuser:appgroup public public
COPY --chown=appuser:appgroup /src /home/appuser/src
COPY --chown=appuser:appgroup . /home/appuser

ENV PYTHONPATH="/home/appuser"

EXPOSE 8000
EXPOSE 9000

USER appuser

ENTRYPOINT []

#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:9000", "--log-level", "DEBUG", "src.app_flask:run_app"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:9000", "--log-level", "DEBUG", "app:app"]




