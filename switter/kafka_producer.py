import json
from django.forms import model_to_dict
from kafka import KafkaProducer

from switter.settings import KAFKA_INTERACTION_TOPIC, KAFKA_POST_TOPIC, KAFKA_URL


class SwitterKafkaProducer:
    _instance: "KafkaProducer | None" = None

    def __new__(cls) -> "SwitterKafkaProducer":
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> "SwitterKafkaProducer":
        self.producer = KafkaProducer(bootstrap_servers=KAFKA_URL)

    def event(self, topic, obj):
        self.producer.send(topic, json.dumps(model_to_dict(obj)).encode())
        self.producer.flush()

    def event_post(self, post):
        self.event(KAFKA_POST_TOPIC, post)

    def event_interaction(self, interaction):
        self.event(KAFKA_INTERACTION_TOPIC, interaction)
