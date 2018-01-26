sleep 5
ip=$(awk 'END{print $1}' /etc/hosts)
secure_url=$(curl "web/?t=2147483647&u=L3MvbGluaw==&ip=$ip&p=password")
nginx_response=$(curl nginx$secure_url)
echo $nginx_response