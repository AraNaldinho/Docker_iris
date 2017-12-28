From ubuntu:latest

LABEL maintainer="Aravind shanmugam <aravindarun1891@gmail.com>"
LABEL Description="Simple Docker Description"
LABEL Simple="workles branch"
ENV http_proxy 43.194.159.120:80
ENV https_proxy 43.194.159.120:80

ADD iris.py /home
ADD download.jpeg /home


