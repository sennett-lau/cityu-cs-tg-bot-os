#! /bin/bash

# Run docker file
docker run -d --name cityu-cs-tg-bot cityu-cs-tg-bot --env-file "$(dirname "$0")/app/.env.dev"