FROM python:3.11

ENV PYTHONBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /bot

COPY . /bot/

RUN pip install -U pip setuptools wheel
RUN pip install -U pdm

RUN pdm sync --prod

CMD ["pdm", "start"]