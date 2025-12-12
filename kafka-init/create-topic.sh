#!/bin/bash

set -e

kafka-topics --create \
  --if-not-exists \
  --topic "${KAFKA_POST_TOPIC}" \
  --bootstrap-server "${KAFKA_URL}" \
  --partitions 1 \
  --replication-factor 1

kafka-topics --create \
  --if-not-exists \
  --topic "${KAFKA_INTERACTION_TOPIC}" \
  --bootstrap-server "${KAFKA_URL}" \
  --partitions 1 \
  --replication-factor 1