FROM python

RUN pip3 install nano-prom-exporter

ENTRYPOINT [ "nano-prom" ]