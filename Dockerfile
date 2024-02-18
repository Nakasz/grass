FROM alpine:3.19.1

# Install dependencies
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN apk add --no-cache chromium chromium-chromedriver unzip
RUN apk add --update --no-cache py3-pip

# Set working directory
WORKDIR /usr/src/app

COPY kons .
RUN pip install --no-cache-dir -r ./requirements.txt --break-system-packages

CMD [ "python", "./main.py" ]
EXPOSE 80