from kafka import KafkaConsumer, KafkaProducer


class KConsumer:
    def __init__(self, topic, bootstrap_servers):
        self.topic = topic
        self.consumer = None
        self.bootstrap_servers = bootstrap_servers

    def consume(self):
        self.consumer = KafkaConsumer(bootstrap_servers=self.bootstrap_servers)
        self.consumer.subscribe(self.topic)
        for msg in self.consumer:
            print(msg)


class KProducer:
    def __init__(self, topic, bootstrap_servers):
        self.producer = None
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers

    def send(self, payload_items):
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
        for item in payload_items:
            item = '{}'.format(item)
            self.producer.send(topic=self.topic, value=bytes(item, encoding='utf-8'))


# Driver Code
# topic = 'quickstart-events'
# bootstrap_servers = 'localhost:9092'

# kp = KProducer(topic, bootstrap_servers)
# kp.send(range(0, 10))

# kc = KConsumer(topic, bootstrap_servers)
# kc.consume()
