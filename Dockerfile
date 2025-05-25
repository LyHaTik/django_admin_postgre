FROM python:3.10.5

RUN mkdir /online_shop

COPY requirements.txt /online_shop/
COPY car_showroom/ /online_shop/

COPY entrypoint.sh /online_shop/
RUN chmod +x /online_shop/entrypoint.sh

WORKDIR /online_shop

RUN pip install -r requirements.txt --no-cache-dir

ENTRYPOINT ["bash", "entrypoint.sh"]