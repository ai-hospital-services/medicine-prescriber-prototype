FROM --platform=linux/arm64 debian:11 AS build

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y apt-transport-https curl file git libglu1-mesa tar unzip xz-utils zip \
        clang cmake ninja-build pkg-config libgtk-3-dev liblzma-dev

WORKDIR /
RUN git clone https://github.com/flutter/flutter.git --depth 1 -b 3.7.12
RUN export PATH="$PATH:/flutter/bin" && flutter precache && flutter config --clear-features && \
    flutter config --enable-web --no-enable-linux-desktop --no-enable-macos-desktop \
        --no-enable-windows-desktop --no-single-widget-reload-optimization --no-enable-android \
        --no-enable-ios --no-enable-fuchsia --no-enable-custom-devices --clear-ios-signing-cert && \
    flutter doctor -v

WORKDIR /frontend
COPY . .

RUN export PATH="$PATH:/flutter/bin" && flutter clean && flutter build web

# ---

FROM --platform=linux/arm64 dart:2.19.6

RUN dart pub global activate dhttpd

WORKDIR /frontend
# COPY build/web build/web
COPY --from=build /frontend/build/web build/web

ARG PORT="80"

ENTRYPOINT ["/root/.pub-cache/bin/dhttpd"]
CMD ["--path", "build/web/", "--host", "0.0.0.0", "--port", ${PORT}]
