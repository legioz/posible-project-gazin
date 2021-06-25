FROM python:3.9.0

LABEL version="1.0.0"
LABEL autor="luizfelipevbll@gmail.com"

ENV DOCKER_ON=True
ENV DEBUG=True
ENV TZ="America/Sao_Paulo"

RUN date
RUN apt-get update && apt-get install -y apt-utils
RUN apt-get install -y gcc \
    zlibc \
    zlib1g-dev \
    libssl-dev \
    libbz2-dev \
    libsqlite3-dev \
    libncurses5-dev \
    libgdbm-dev \
    libgdbm-compat-dev \
    liblzma-dev \
    libreadline-dev \
    libffi-dev \
    uuid-dev \
    apt-transport-https \
    ca-certificates \
    man \
    curl \
    wget \
    vim \
    nano \
    wget \
    gnupg2 \
    default-libmysqlclient-dev \
    build-essential \
    python3-pip \
    bash-completion \
    tree \
    neofetch \
    libmariadb-dev \
    && apt-get autoremove -y \
    && apt-get autoclean -y


RUN mkdir -p /home/src
WORKDIR /home/src/

COPY ./ /home/src

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt 

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
