# NGNIX Conf

1. install nginx

```sh
sudo apt install nginx
```

2. copy the static content

```sh
#replace user for your user
sudo cp -r ~user/dark-resolver/resolver/static /usr/share/nginx/html/
```

2. create a folder for 

```sh
sudo mkdir /etc/nginx/shared-locations/
```

3. copy the location conf files
```sh
sudo cp -r ~user/dark-resolver/docker/*.conf  /etc/nginx/shared-locations/
```

4. Replace the default ngnix conf
```sh
sudo rm /etc/ngnix/sites-enable/default
sudo cp ~user/dark-resolver/docker/ngnix-default  /etc/ngnix/sites-enable/default
```

5. check and rstart ngnix
```sh
#check nginx configuration
sudo  nginx -t
sudo  systemctl restart nginx
```