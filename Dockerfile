FROM python:3.9-alpine

RUN apk update && apk add chromium chromium-chromedriver

ARG project_dir=/python/app/
ADD requirements.txt ${project_dir}
WORKDIR ${project_dir}

RUN set -x && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

ADD . ${project_dir}

CMD ["python3", "main.py"]