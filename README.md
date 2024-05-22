https://github.com/rabbitmq/rabbitmq-server/discussions/11262#discussioncomment-9523092

## Setup

* Run `pipenv install` to setup the necessary Python libraries.
* Run `pipenv shell` to activate those libraries in your current shell session.

## Reproduction

1) start rmq 3.12 by up312.sh script
2) publish 10 messages in mqtt with publishMqtt.py
3) read messages with readAmqp.py timestamp is available for all messages
4) read messages with readStream.py timestamp is not available
5) down server with down312.sh
6) upgrade server with up313.sh
7) read messages with readAmqp.py timestamp is available for all messages
8) read messages with readStream.py timestamp is not available
9) publish 10 messages in mqtt with publishMqtt.py
10) read messages with readAmqp.py timestamp is available for all messages
11) read messages with readStream.py timestamp is  only available for 10 last messages
