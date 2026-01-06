import json
import logging
import threading
from typing import Any, ClassVar

from django.forms import model_to_dict
from kafka import KafkaProducer

from switter.settings import KAFKA_URL


class SwitterKafkaProducer:
    _producer: ClassVar[KafkaProducer | None] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    @classmethod
    def get_producer(cls):
        if cls._producer is None:
            with cls._lock:
                if cls._producer is None:
                    cls._producer = KafkaProducer(
                        bootstrap_servers=KAFKA_URL,
                        retries=3,
                        linger_ms=10,
                    )
        return cls._producer

    @classmethod
    def event(cls, topic: str, value: Any, action: str):
        try:
            producer = cls.get_producer()
            data = json.dumps(model_to_dict(value) | {"action": action}).encode()
            producer.send(topic, data)
        except Exception as e:
            logging.error("Error: Can not send to kafka server", exc_info=e)
