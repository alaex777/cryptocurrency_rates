FROM python:3.11

WORKDIR /opt

RUN apt-get update && apt-get install -y curl git

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080
EXPOSE 4000

HEALTHCHECK --interval=5s --timeout=5s --retries=5 --start-period=5s CMD curl -f 0.0.0.0:4000/ping/cryptocurrency_rates || exit 1

CMD ["python", "run.py"]