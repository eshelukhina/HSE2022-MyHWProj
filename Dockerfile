FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./web_server /code/web_server
COPY ./main.py /code

COPY ./database /code/database
COPY ./result_listener /code/result_listener
COPY ./runner /code/runner