# NETWORK TOOLS


## IP

### ifconfig

> NOTE: Unix/iOS

Show additional info for `en0` interface:
```
ifconfig -v en0

    en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500 index 5
      eflags=412008c0<ACCEPT_RTADV,TXSTART,ARPLL,NOACKPRI,ECN_ENABLE,FASTLN_ON>
      ether d0:a6:37:ec:7f:71 
      inet6 fe80::1c24:564a:66f1:b008%en0 prefixlen 64 secured scopeid 0x5 
      inet 192.168.149.137 netmask 0xffffff00 broadcast 192.168.149.255
      nd6 options=201<PERFORMNUD,DAD>
      media: autoselect
      status: active
      type: Wi-Fi
      link quality: 100 (good)
      state availability: 0 (true)
      scheduler: FQ_CODEL (driver managed)
      uplink rate: 31.97 Mbps [eff] / 304.20 Mbps
      downlink rate: 31.97 Mbps [eff] / 304.20 Mbps [max]
      qosmarking enabled: yes mode: none
```

### ip

> NOTE: The new substitution of deprecated `ifconfig` tool on modern Unix

Show the same amount of info that `ifconfig` shows
```
ip a
```


## DNS

### nslookup

Find IP mapped to DNS record
```
nslookup ukr.net

    Server:		192.168.149.132
    Address:	192.168.149.132#53

    Non-authoritative answer:
    Name:	ukr.net
    Address: 104.18.8.128
    Name:	ukr.net
    Address: 104.18.9.128
```

Find DNS record mapped to IP 
> NOTE: Only if the reverse lookup zone has been set up properly
```
nslookup 216.58.209.14

    Server:		192.168.149.132
    Address:	192.168.149.132#53

    Non-authoritative answer:
    14.209.58.216.in-addr.arpa	name = sof01s12-in-f14.1e100.net.
    14.209.58.216.in-addr.arpa	name = waw02s18-in-f14.1e100.net.

# OR
    
nslookup
> set type=PTR
> 216.58.209.14

    Server:		192.168.149.132
    Address:	192.168.149.132#53

    Non-authoritative answer:
    14.209.58.216.in-addr.arpa	name = sof01s12-in-f14.1e100.net.
    14.209.58.216.in-addr.arpa	name = waw02s18-in-f14.1e100.net.

    Authoritative answers can be found from:
```


## Scan Remote Server to find: open ports, OS, etc

### nmap (network map)

Use `nmap` tool
```
nmap -sS -O <IP_of_remote_server>
```

### zenmap
Same as `nmap`, but with UI.











