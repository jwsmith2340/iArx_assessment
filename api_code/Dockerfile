FROM python:3.11

WORKDIR /opt/iarx

COPY requirements.txt .
COPY ./common/ /opt/iarx/common/
COPY ./main.py /opt/iarx/main.py
COPY ./seed_data.py /opt/iarx/seed_data.py

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]