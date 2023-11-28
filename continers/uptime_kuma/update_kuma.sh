#!/bin/bash

# Update the system and Podman
sudo dnf update -y podman

# Pull the latest image for Uptime Kuma from Docker Hub
podman pull docker.io/louislam/uptime-kuma:1

# Identify the running Uptime Kuma container
container_id=$(podman ps -a --filter "ancestor=docker.io/louislam/uptime-kuma:1" --format="{{.ID}}")

# Check if container_id is non-empty
if [[ -z "$container_id" ]]; then
    echo "No running Uptime Kuma container found. Checking for stopped containers..."
    container_id=$(podman ps -a --filter "ancestor=docker.io/louislam/uptime-kuma:1" --format="{{.ID}}" --filter status=exited)
    if [[ -z "$container_id" ]]; then
        echo "No Uptime Kuma container found."
        exit 1
    fi
fi

# Stop the current container if it's running
podman stop $container_id

# Backup the old container
backup_name="${container_id}_backup"
podman rename $container_id $backup_name

# Remove any existing container named 'uptime-kuma'
if podman ps -a --filter "name=uptime-kuma" --format="{{.ID}}" | grep -q .; then
    podman rm uptime-kuma
fi

# Run the new container instance with the latest image
if podman run -d --name uptime-kuma -p 3001:3001 -v /home/devops/uptime-kuma/uptime-data:/app/data docker.io/louislam/uptime-kuma:1; then
    echo "New Uptime Kuma container started successfully."
else
    echo "Failed to start new Uptime Kuma container."
    exit 1
fi

# Optional: Verify the new container is up and running correctly

# Cleanup (Optional). Uncomment to automatically delete the backup container.
# podman rm $backup_name