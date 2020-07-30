
#!/bin/sh

apt-get update
mkdir ~/.ssh
mkdir -p /var/run/sshd
chmod 600 ~/.ssh
chmod 600 /etc/ssh/*
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
echo $pub_key >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
service ssh restart
touch /etc/nginx/upstreams.conf
touch /etc/nginx/servers.conf
### to be removed
redis-server --daemonize yes
### 
openssl req -nodes -x509 -newkey rsa:4096 -keyout /etc/nginx/key.pem -out /etc/nginx/cert.pem -days 365 -subj '/CN=localhost'
service nginx restart
cd /services
python3 /services/lbd.py &
python3 /services/app.py
