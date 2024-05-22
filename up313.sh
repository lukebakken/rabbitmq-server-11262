#!/bin/bash

docker compose -f rmq313.yml --verbose up --no-build --pull missing -d


cpt=0
until [[ `docker inspect -f {{.State.Running}} rabbitmq` == true ]] || [[ $cpt -lt 10 ]]
do
    sleep 1s;
    echo "waiting for rabbitmq container..."
    ((cpt++))
done

sleep 5s;

docker exec rabbitmq rabbitmqctl await_startup
docker exec rabbitmq rabbitmqctl list_feature_flags
docker exec rabbitmq rabbitmqctl enable_feature_flag detailed_queues_endpoint
docker exec rabbitmq rabbitmqctl enable_feature_flag message_containers
docker exec rabbitmq rabbitmqctl enable_feature_flag mqtt_v5
docker exec rabbitmq rabbitmqctl enable_feature_flag quorum_queue_non_voters
docker exec rabbitmq rabbitmqctl enable_feature_flag rabbit_mqtt_qos0_queue
docker exec rabbitmq rabbitmqctl enable_feature_flag restart_streams
docker exec rabbitmq rabbitmqctl enable_feature_flag stream_filtering
docker exec rabbitmq rabbitmqctl enable_feature_flag stream_sac_coordinator_unblock_group
docker exec rabbitmq rabbitmqctl enable_feature_flag stream_update_config_command
docker exec rabbitmq rabbitmqctl list_feature_flags

