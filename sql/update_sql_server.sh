#!/bin/bash

# Pull the latest image
docker pull custom-sql-server

# Stop the current container
docker stop sql_server_demo

# Remove the current container
docker rm sql_server_demo

# Run a new container with the same settings
docker run -d \
  --name sql_server_demo \
  --hostname sqldevops \
  -e 'ACCEPT_EULA=Y' \
  -e 'SA_PASSWORD=DevSecOps1' \
  -e 'MSSQL_PID=Express' \
  -e 'MSSQL_MEMORY_LIMIT_MB=1024' \
  -p 1433:1433 \
  custom-sql-server
