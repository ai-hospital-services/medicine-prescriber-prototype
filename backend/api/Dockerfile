FROM --platform=linux/arm64 python:3.10.10-slim-buster

WORKDIR /backend
COPY . api

RUN apt-get update && apt-get upgrade -y && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r ./api/requirements.txt

ARG FLASK_DEBUG="1"
ENV FLASK_DEBUG=${FLASK_DEBUG}

ARG MONGODB_URL="mongodb://localhost:27017/"
ENV MONGODB_URL=${DB_CONNECTION_URL}

ARG TENANT_DOMAIN="<TENANT DOMAIN>"
ENV TENANT_DOMAIN=${TENANT_DOMAIN}

ARG REDIRECT_URL="http://localhost:9090/auth.html"
ENV REDIRECT_URL=${REDIRECT_URL}

ARG CLIENT_ID="<CLIENT ID>"
ENV CLIENT_ID=${CLIENT_ID}

ARG CLIENT_SECRET="<CLIENT SECRET>"
ENV CLIENT_SECRET=${CLIENT_SECRET}

ENTRYPOINT [ "./api/entrypoint.sh" ]
CMD ["migrateThenApi"]
