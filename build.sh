#!/bin/bash


tag='latest'

# Export env var previously with:
# export NLQ_ECS_REPOSITORY=......

# shellcheck disable=SC2162
read -p "IMAGE_TAG [latest]: " tag
export IMAGE_TAG=$tag

aws ecr get-login-password --region us-east-1 |
docker login --username AWS --password-stdin "$NLQ_ECS_REPOSITORY"

docker build -f Dockerfile  --platform linux/amd64 -t nlq-on-aws .
docker tag nlq-on-aws "$NLQ_ECS_REPOSITORY":"$IMAGE_TAG"
docker push "$NLQ_ECS_REPOSITORY":"$IMAGE_TAG"
