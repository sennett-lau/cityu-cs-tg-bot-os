#! /usr/bin/bash

docker rm $(docker stop $(docker ps -a -q --filter ancestor=cityu-cs-tg-bot --format="{{.ID}}"))
docker rmi cityu-cs-tg-bot:latest
docker build -t cityu-cs-tg-bot:latest .
docker run -d --name cityu-cs-tg-bot cityu-cs-tg-bot
