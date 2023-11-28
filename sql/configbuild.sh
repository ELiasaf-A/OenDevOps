docker run -d \
  --name sql_server_demo \
  -e 'ACCEPT_EULA=Y' \
  -e 'SA_PASSWORD=DevSecOps1' \
  -e 'MSSQL_MEMORY_LIMIT_MB=1024' \
  -p 1433:1433 \
  omjee/sqlserver2022
