FROM python:3.9.13-slim-buster

WORKDIR /backend
COPY . api

RUN apt-get update && apt-get upgrade && \
    pip install --upgrade pip && \
    pip install -r ./api/requirements.txt

ARG FLASK_DEBUG="1"
ENV FLASK_DEBUG=${FLASK_DEBUG}

ARG MONGODB_URL="mongodb://localhost:27017/"
ENV MONGODB_URL=${DB_CONNECTION_URL}

ENTRYPOINT [ "./api/entrypoint.sh" ]
CMD ["migrateThenApi", "--debug-mode", "false"]
