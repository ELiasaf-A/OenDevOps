#!/bin/bash

# Update the system and Podman
sudo dnf update -y podman

# Define the image name for your proxy server
IMAGE_NAME="jc21/nginx-proxy-manager:latest"

# Pull the latest image for your proxy server
podman pull $IMAGE_NAME

# Find the running container's ID for the proxy server
container_id=$(podman ps -q --filter ancestor=$IMAGE_NAME)

# Stop the old container
podman stop $container_id

# Rename the old container (this is to keep it for rollback purposes in case the new container has issues)
podman rename $container_id "${container_id}_backup"

# Create and run a new container based on the latest image
# Replace the ... with your volume mounts, ports, and other configurations
podman run -d \
  --name nginx-proxy-manager \
  -p 80:80 \
  -p 443:443 \
  -p 81:81 \
  -v ./data:/data
  -v ./letsencrypt:/etc/letsencrypt

  $IMAGE_NAME

# Optionally, if everything is running smoothly after some time, you can remove the old container
podman rm "${container_id}_backup"