#! /bin/bash
set -euo pipefail
./build.sh

TAG=$(git rev-parse HEAD | cut -c1-10)
IMAGE="infuseai/dataset-upload-web-front-end:${TAG}"
echo "pusblish image at $IMAGE"
docker tag dataset-upload-web-front-end $IMAGE
docker push $IMAGE
