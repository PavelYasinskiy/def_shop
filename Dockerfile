FROM python:3.11

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./data_base /data_base
COPY ./keyboards /keyboards
COPY ./media /media
COPY ./main.py /main.py
COPY ./.env /.env
COPY ./requirements.txt /requirements.txt
COPY ./docker-compose.yml /docker-compose.yml

WORKDIR /

EXPOSE 80

RUN pip install -r requirements.txt

CMD ["python", "main.py"]

