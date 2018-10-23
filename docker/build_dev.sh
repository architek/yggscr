docker-compose -f docker/docker-compose-dev.yml build --build-arg BUILD_DATE=$(date -u +%Y-%m-%dT%H:%M:%S) stage-dev
