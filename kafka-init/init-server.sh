#!/bin/bash

set -e

KAFKA_CLUSTER_ID="$($KAFKA_PATH/bin/kafka-storage.sh random-uuid)"
$KAFKA_PATH/bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c $KAFKA_CONFIG_PATH/server.properties
$KAFKA_PATH/bin/kafka-server-start.sh $KAFKA_CONFIG_PATH/server.properties