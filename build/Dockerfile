FROM debian:trixie-20260112-slim

RUN apt-get update && \
    apt-get install -y pandoc=3.1.11.1+ds-2 unzip=6.0-29 && \
    apt-get clean

COPY compile-html md-link-to-html.lua /build-scripts/
WORKDIR /build-scripts

CMD ["bash", "compile-html", "/markdown", "/html-template", "/out-dir"]
