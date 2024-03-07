FROM python:3

ENV API_KEY=[azitek_key]
ENV GATEWAY_ID="187723572702721"
ENV START_DATE="2023-11-17T10:00:00"
ENV END_DATE="2023-11-18T17:00:00"

COPY desafio-backend.py /app/desafio-backend.py
WORKDIR /app
RUN pip install matplotlib

CMD ["python", "desafio-backend.py"]
