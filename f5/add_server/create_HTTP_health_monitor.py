# Health Monitor Details
monitor_name = 'http_monitor'
monitor_partition = 'Common'  # Change if you are using a different partition
monitor_send = 'GET / HTTP/1.1\\r\\nHost: www.example.com'  # Modify as needed
monitor_recv = '200 OK'  # Expected response string, modify as needed

# Create an HTTP health monitor
http_monitor = mgmt_root.tm.ltm.monitor.https.http.create(
    name=monitor_name,
    partition=monitor_partition,
    sendString=monitor_send,
    recvString=monitor_recv
)
