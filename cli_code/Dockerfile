FROM python:3.11

WORKDIR /opt/iarx

COPY ./cli.py /opt/iarx/cli.py

RUN pip install --no-cache-dir requests

CMD ["python", "/opt/iarx/cli.py"]