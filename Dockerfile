FROM python:alpine3.20

# install dependencies
RUN apk update
RUN apk add gcc \
        openjdk11 \
        wget \
        unzip \
        git \
        alpine-sdk
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        libc-dev \
        linux-headers \
        postgresql-dev  && apk add libffi-dev

# downlaod RMiner
RUN wget "https://github.com/tsantalis/RefactoringMiner/releases/download/3.0.9/RefactoringMiner-3.0.9.zip"

RUN unzip RefactoringMiner-3.0.9.zip -d /RMiner

WORKDIR /miner
RUN mkdir components

ADD components ./components

COPY requirements.txt ./
COPY config.ini ./
COPY main.py ./

RUN mkdir ./output
RUN mkdir ./cloned_repos

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
