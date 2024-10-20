FROM python:3.8-alpine

RUN apk --update-cache add --virtual build-dependencies build-base linux-headers git

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt \
    && python setup.py install \
    && apk del build-dependencies

# Use python to run the nano-prom module
ENTRYPOINT ["python", "-m", "nano_prom_exporter"]