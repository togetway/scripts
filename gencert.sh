#!/bin/sh

# create self-signed server certificate:

read -p "Enter your domain [www.example.com]: " DOMAIN

echo "Create server key..."

openssl genrsa -des3 -out $DOMAIN.key 1024

echo "Create server certificate signing request..."

SUBJECT="/C=CN/ST=GZ/L=IT/O=IT/OU=IT/CN=$DOMAIN"

openssl req -new -subj $SUBJECT -key $DOMAIN.key -out $DOMAIN.csr

echo "Remove password..."

mv $DOMAIN.key $DOMAIN.origin.key
openssl rsa -in $DOMAIN.origin.key -out $DOMAIN.key

echo "Sign SSL certificate..."

openssl x509 -req -days 3650 -in $DOMAIN.csr -signkey $DOMAIN.key -out $DOMAIN.crt

cat <<EOF
TODO:
Copy $DOMAIN.crt to /etc/nginx/ssl/$DOMAIN.crt
Copy $DOMAIN.key to /etc/nginx/ssl/$DOMAIN.key
Add configuration in nginx:
server {
    ...
    ssl on;
    ssl_certificate     /etc/nginx/ssl/$DOMAIN.crt;
    ssl_certificate_key /etc/nginx/ssl/$DOMAIN.key;
}
EOF