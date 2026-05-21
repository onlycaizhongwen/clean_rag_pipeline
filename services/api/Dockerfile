ARG PYTHON_BASE_IMAGE=docker.m.daocloud.io/library/python:3.12-slim
FROM ${PYTHON_BASE_IMAGE}

ARG PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV PIP_INDEX_URL=${PIP_INDEX_URL}

WORKDIR /app
COPY pyproject.toml /app/
COPY app /app/app
COPY alembic.ini /app/alembic.ini
COPY migrations /app/migrations
RUN pip install --no-cache-dir setuptools wheel \
    && pip install --no-cache-dir --no-build-isolation .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
