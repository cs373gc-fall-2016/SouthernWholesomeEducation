sudo pkill supervisord
sudo /usr/local/bin/supervisord -c supervisord.conf
sudo /usr/local/bin/supervisorctl -c supervisord.conf status
