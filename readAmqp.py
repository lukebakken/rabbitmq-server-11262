import logging
import pika
import os
import datetime
import sys, getopt

credentials = pika.PlainCredentials("myuser", "password")
params = pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)

COUNT = 0


def main(argv):
    connection = pika.BlockingConnection(params)  # Connect to server
    channel = connection.channel()  # start a channel
    channel.basic_qos(prefetch_count=100, global_qos=False)
    stream = "MYQUEUE.stream"
    arguments = {"x-stream-offset": "first"}
    channel.basic_consume(
        stream,
        on_message_callback,
        auto_ack=False,
        exclusive=False,
        consumer_tag=False,
        arguments=arguments,
    )

    channel.start_consuming()

    connection.close()


# create a function which is called on incoming messages
def on_message_callback(channel, method_frame, header_frame, body):
    # print(method_frame)
    # print(header_frame)

    global start
    global COUNT

    COUNT = COUNT + 1
    timestamp = header_frame.headers.get("timestamp_in_ms")
    key = method_frame.routing_key
    print(f"timestamp: {timestamp} key: {key} body: {body}")
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == "__main__":
    main(sys.argv[1:])
