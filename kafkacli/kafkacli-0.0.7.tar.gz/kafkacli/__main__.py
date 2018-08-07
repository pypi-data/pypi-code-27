#!/usr/bin/env python
import argparse
import threading, logging, time
import multiprocessing
import ConfigParser
import sys
from kafka import KafkaConsumer, KafkaProducer
from kafkacli import util
from argparse import RawTextHelpFormatter

class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers=options.broker,
                                 retries=5)

        while not self.stop_event.is_set():
            user_input = raw_input()
            producer.send(options.topic, user_input)

        producer.close()

class Consumer(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        
    def stop(self):
        self.stop_event.set()
        
    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=options.broker,
                                 auto_offset_reset=options.offset,
                                 consumer_timeout_ms=1000)
        consumer.subscribe([options.topic])

        while not self.stop_event.is_set():
            for message in consumer:
                print(message.value)
                if self.stop_event.is_set():
                    break

        consumer.close()
        
def get_topics():
    return KafkaConsumer(bootstrap_servers=options.broker).topics()
    
def _parse_arguments():
    parser = argparse.ArgumentParser(description=util.DESCRIPTION, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-m', '--mode', help="Mode: consume, produce, list")
    parser.add_argument('-b', '--broker', help="Kafka broker endpoint")
    parser.add_argument('-t', '--topic', help="Kafka topic to consume from or produce to")
    parser.add_argument('-o', '--offset', default="latest", help="Offset mode: earliest, latest (default: 'latest')")
    parser.add_argument('-V', '--version', action='store_true', help="Display kafkacli version")

    # global options
    global options
    options = parser.parse_args()

    if options.version:
        util.show_version()
    elif options.mode:
        if options.mode not in ["consume", "produce", "list"]:
            print "Please provide one of the following modes: consume, produce, list"
            sys.exit(1)
        elif not options.broker:
            print "Please provide broker endpoint"
            sys.exit(1)
        else:
            util.print_dashed_line()
            print("Mode: {}".format(options.mode))
            print("Broker: {}".format(options.broker))
            if options.mode in ["consume", "produce"]:
                print("Topic: {}".format(options.topic))
            if options.mode == "consume":
                print("Offset: {}".format(options.offset))
            util.print_dashed_line()
            
    return options

def main():

    _parse_arguments()

    if options.mode == "produce":
        producer_task = Producer()
        producer_task.start()
        producer_task.join()
    elif options.mode == "consume":
        consumer_task = Consumer()
        consumer_task.start()
        consumer_task.join()
    elif options.mode == "list":
        topics = get_topics()
        print("\n".join(str(topic) for topic in topics))
        
        
if __name__ == "__main__":
    main()