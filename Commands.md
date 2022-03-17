# NETWORK TOOLS


## IP info

### ifconfig

Show additional info for `en0` interface (Unix/iOS):
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


## Scan Remote Server to find: open ports, OS, etc

### nmap (network map)

Use `nmap` tool
```
nmap -sS -O <IP_of_remote_server>
```

### zenmap
Same as `nmap`, but with UI.











