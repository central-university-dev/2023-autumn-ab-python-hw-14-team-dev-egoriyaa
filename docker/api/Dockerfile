FROM python:3.10

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
RUN apt-get update && apt-get install libgl1 -y
RUN pip install poetry

COPY . .

RUN poetry install
