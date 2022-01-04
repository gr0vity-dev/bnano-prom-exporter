FROM python:3.7

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY nano_prom_exporter/ nano_prom_exporter/

ENTRYPOINT [ "python", "-m", "nano_prom_exporter" ]