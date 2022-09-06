# FROM --platform=linux/arm64 debian:10.2 AS build

# RUN apt-get update && apt-get upgrade -y && \
#     apt-get install -y apt-transport-https curl file git \
#     libglu1-mesa tar unzip xz-utils zip \
#     clang cmake ninja-build pkg-config libgtk-3-dev liblzma-dev

# RUN git clone --depth 1 --branch 3.3.1 https://github.com/flutter/flutter.git && \
#     export PATH="$PATH:`pwd`/flutter/bin" && flutter config --clear-features && \
#     flutter config --enable-web --no-enable-linux-desktop --no-enable-macos-desktop \
#     --no-enable-windows-desktop --no-single-widget-reload-optimization --no-enable-android \
#     --no-enable-ios --no-enable-fuchsia --no-enable-custom-devices --clear-ios-signing-cert \
#     && flutter doctor -v

# WORKDIR /frontend
# COPY . .

# RUN flutter clean && flutter build web

# ---

FROM --platform=linux/arm64 dart:2.18.0

RUN dart pub global activate dhttpd

WORKDIR /frontend
COPY build/web build/web
# COPY --from=build build/web build/web

ARG PORT="80"

ENTRYPOINT ["/root/.pub-cache/bin/dhttpd"]
CMD ["--path", "build/web/", "--host", "0.0.0.0", "--port", ${PORT}]
