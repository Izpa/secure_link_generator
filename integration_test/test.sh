sleep 5
ip=$(awk 'END{print $1}' /etc/hosts)
secure_url=$(curl "web/?t=2147483647&u=L3MvbGluaw==&ip=$ip&p=password" --silent)
nginx_response=$(curl nginx$secure_url --silent)
echo $nginx_response