FROM ghcr.io/charmbracelet/vhs:latest

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
    && python3 -m pip install --break-system-packages uv \
    && mv /usr/local/bin/uv /usr/local/bin/uv-real \
    && rm -rf /var/lib/apt/lists/*

COPY assets/vhs-uv /usr/local/bin/uv
RUN chmod +x /usr/local/bin/uv
