#!/bin/bash

docker compose -f rmq312.yml --verbose up --no-build --pull missing -d

