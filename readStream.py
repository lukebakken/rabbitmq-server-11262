import logging
import os
import datetime
import sys, getopt
import asyncio

from rstream import (
    AMQPMessage,
    Consumer,
    MessageContext,
    ConsumerOffsetSpecification,
    OffsetType,
    OnClosedErrorInfo,
    amqp_decoder,
)


async def consume():
    async def on_connection_closed(disconnection_info: OnClosedErrorInfo) -> None:
        print(
            "connection has been closed from stream: "
            + str(disconnection_info.streams)
            + " for reason: "
            + str(disconnection_info.reason)
        )

        global connection_is_closed

        # avoid multiple simultaneous disconnection to call close multiple times
        if connection_is_closed is False:
            await consumer.close()
            connection_is_closed = True

    consumer = Consumer(
        host="localhost",
        port=5552,
        vhost="/",
        username="myuser",
        password="password",
        on_close_handler=on_connection_closed,
    )

    loop = asyncio.get_event_loop()
    # loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(consumer.close()))

    async def on_message(msgss: AMQPMessage, message_context: MessageContext):
        print(
            "Timestamp {} Key {} Body {}".format(
                msgss.message_annotations.get(b"x-opt-rabbitmq-received-time"),
                msgss.message_annotations.get(b"x-routing-key"),
                msgss.get_data(),
            )
        )

    await consumer.start()
    # await consumer.subscribe(stream=STREAM, callback=on_message, decoder=amqp_decoder)
    await consumer.subscribe(
        stream="MYQUEUE.stream",
        callback=on_message,
        offset_specification=ConsumerOffsetSpecification(OffsetType.FIRST),
        initial_credit=1000,
        decoder=amqp_decoder,
    )
    await consumer.run()


try:
    asyncio.run(consume())
except KeyboardInterrupt:
    print("Exiting...")
