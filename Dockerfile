FROM alpine:3.6

COPY ./agg-2.5-r0.apk /opt/packages/agg-2.5-r0.apk
COPY ./agg-dev-2.5-r0.apk /opt/packages/agg-dev-2.5-r0.apk

RUN \
    echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories; \
    apk add --no-cache --allow-untrusted --virtual .build-deps \
        python-dev \
        gdal-dev \
        potrace-dev \
        sdl-dev \
        libx11 \
        build-base \
        py-numpy-dev \
    ; \
    apk add --no-cache --allow-untrusted \
        py-numpy \
        potrace \
        gdal \
        python \
        py-pip \
        git \
        py-gdal \
        py-six \
        py-click \
        py-enum34 \
        /opt/packages/agg-dev-2.5-r0.apk \
        /opt/packages/agg-2.5-r0.apk \
    ; \
    pip install \
        glob2 \
        pyproj \
        fiona \
        gippy \
        pypotrace \
    ; \
    git clone https://github.com/venicegeo/beachfront-py; \
    cd beachfront-py; \
    python setup.py build_ext --inplace; \
    python setup.py install; \
    apk del .build-deps; \
    rm /opt/packages/agg*; \
    cd /; \
    rm -rf beachfront-py

ADD ./bin /
