# Receive UDP to local socket


## In terminal 1
Start python script to:
- Start listen to port `9090` for inbound `UDP` connection on all `IP` adresses, assigned to the server


## In terminal 2
Start `Client` that will send data you type, to port `9090` with `IP` of your server via `UDP` connection
```
# MacOS
nc -u 192.168.149.137 9090
```


## In terminal 1

Message from the `Client` should appear

