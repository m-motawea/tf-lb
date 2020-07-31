
#!/bin/sh

apt-get update
mkdir ~/.ssh
mkdir -p /var/run/sshd
chmod 600 ~/.ssh
chmod 600 /etc/ssh/*
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
echo $SSH_KEY >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
service ssh restart
touch /etc/nginx/upstreams.conf
touch /etc/nginx/servers.conf
### to be removed
redis-server --daemonize yes
### 
openssl req -nodes -x509 -newkey rsa:4096 -keyout /etc/nginx/key.pem -out /etc/nginx/cert.pem -days 365 -subj '/CN=localhost'
cd /services
chmod +x /trc
chmod +x /failover.sh

python3 /services/clusterd.py &
python3 /services/lbd.py &
service nginx restart

python3 /services/app.py
