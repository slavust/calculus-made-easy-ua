FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y python3 \
                       texlive \
                       texlive-lang-cyrilic \
                       gladtex \
                       pandoc && \
    apt-get clean

#COPY compile-html.py compile-epub-mathml.py compile-epub-svg.py compile-pdf.py compile-all.py /build-scripts/
COPY compile-html.py /build-scripts/
WORKDIR /build-scripts

CMD ["python3", "compile-html.py"]
