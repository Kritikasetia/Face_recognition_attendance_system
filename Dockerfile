FROM python:3.8-slim-buster

# Install Dependencies
RUN apt-get -y update && apt-get install -y --fix-missing \
    build-essential \
    gcc \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

# Install Dependencies for opencv
RUN apt-get install ffmpeg libsm6 libxext6  -y

# Virtual Environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV CFLAGS=-static

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


# Add our packages
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY . .

RUN ls

CMD python3 face_recognition_web.py