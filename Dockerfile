FROM ubuntu:18.04
RUN echo deb http://be.archive.ubuntu.com/ubuntu/ bionic main restricted universe multiverse > /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y openssh-client openssh-server nginx keepalived python3-pip vim
COPY services /services
RUN pip3 install -r /services/requirements.txt
COPY start.sh /start.sh
COPY services/lib/templates/nginx.conf /etc/nginx/nginx.conf
COPY failover.sh /failover.sh
COPY trc /trc
RUN chmod +x /start.sh
ENTRYPOINT ["/bin/bash", "/start.sh"]