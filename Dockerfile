FROM python:alpine3.20

# install dependencies
RUN apk update
RUN apk add gcc \
        openjdk11 \
        wget \
        unzip \
        git
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
COPY get_github_url.py ./
COPY get_commit_diff.py ./
COPY effort_test.py ./
COPY developers_effort.py ./
COPY refactoring_miner.py ./
COPY utility.py ./

RUN mkdir ./output
RUN mkdir ./cloned_repos
RUN apk add alpine-sdk
RUN pip3 install -r requirements.txt

COPY config.ini ./
COPY index.py ./
CMD ["python3", "main.py"]
