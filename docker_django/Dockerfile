FROM python:3.10.5-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /online_shop

COPY ./online_shop /online_shop/
COPY ./docker_django/entrypoint.sh /online_shop/entrypoint.sh

RUN chmod +x /online_shop/entrypoint.sh

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN apt-get update && apt-get install -y netcat


ENTRYPOINT ["bash", "entrypoint.sh"]
