# Secure link generator

Web-api, which generates nginx secure link for parameters

## Requirements
Python 3.6

Flask 0.12.2

## Download

## Installation
In virtualenv run

```
pip install -r requirements.txt
```

Then you must set environment variable APP_SETTINGS (development, testing, staging or production), FLASK_APP (run.py)
and SECRET (random string)

```
export APP_SETTINGS="development"
export FLASK_APP="run.py"
export SECRET="some_random_string"
```

And then run the web-application

```
flask run
```

Now web-application running on http://127.0.0.1:5000/

Also you can use docker file in project root (you also must set environment variables for your container)

## Usage example

Api receives next parameters:

t - secure link expiration time (unix timestamp, positive integer, required)
u - url base64 coded (url can be valid url or unix path string, required)
ip - ip v4 address from where the request will be sent (string, required)
p - password (string, required)

Request example

```
http://127.0.0.1:5000/?t=2147483647&u=L3MvbGluaw==&ip=127.0.0.1&p=password
```

Response example

```
/s/link?md5=FbRZ_kL2P7SJMI6hCxS11Q&expires=2147483647
```

## Run unit tests

```
python -m unittest discover
```

## Run simple integration test

This test run this web-application, nginx-server and test bash-script in different docker-containers

Test script sends request with correct parameters to api, receives url and sends get-request to this url

nginx-server location
```
set $p "password";
location /s/ {
    secure_link $arg_md5,$arg_expires;
    secure_link_md5 "$secure_link_expires$uri$remote_addr=$p";
    if ($secure_link = "") { return 403; }
    if ($secure_link = "0") { return 410; }

    return 200 "OK!";
}
```

Requires installed docker and docker-compose

If you want change some settings (e.g. container port) you can change integration_test/docker-compose.yml

Run in project directory

```
docker-compose -f integration_test/docker-compose.yml build
docker-compose -f integration_test/docker-compose.yml -p ci up -d
docker logs -f ci_sut_1
```

Output example

```
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    53  100    53    0     0   5570      0 --:--:-- --:--:-- --:--:--  6625
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100     3  100     3    0     0    341      0 --:--:-- --:--:-- --:--:--   375
OK!

```