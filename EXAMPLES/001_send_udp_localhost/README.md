# Send UDP to local socket


## In terminal 1

Start listen to port `9090` for inbound `UDP` connection
```
# MacOS
nc -luv 9090
```


## In terminal 2
Start python script to:
- send `Hello, world` to local server on port `9090` via `UDP` connection

