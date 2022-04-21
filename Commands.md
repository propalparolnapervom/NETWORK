# NETWORK TOOLS

[Docs: `ip` tool](https://access.redhat.com/sites/default/files/attachments/rh_ip_command_cheatsheet_1214_jcs_print.pdf)

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

### arp

> NOTE: To see `MAC Adress` -> `IP` mapping

Show `arp cache`
```
arp -a
? (192.168.149.132) at 72:d5:50:f9:de:67 on en0 ifscope [ethernet]
? (192.168.149.137) at d0:a6:37:ec:7f:71 on en0 ifscope permanent [ethernet]
? (192.168.149.255) at ff:ff:ff:ff:ff:ff on en0 ifscope [ethernet]
? (224.0.0.251) at 1:0:5e:0:0:fb on en0 ifscope permanent [ethernet]
? (239.255.255.250) at 1:0:5e:7f:ff:fa on en0 ifscope permanent [ethernet]
broadcasthost (255.255.255.255) at ff:ff:ff:ff:ff:ff on en0 ifscope [ethernet]
```

### route

> NOTE: To view and manipulate `IP routing table`

> NOTE: We can work with `IP routing table` on your OS, as `router` is built in

Show route table
```
route -n
```

### netstat

Show network statistic
```
netstat
```

Show overall statistic
```
netstat -s
```
Show route table
```
netstat -rn
```


## TCP/UDP

### nc

> NOTE: networking utility for reading from and writing to network connections using TCP or UDP

View keys
```
nc -help
```

On a local machine, start listening server
```
# MacOS

# Listen for UDP in verbose mode
nc -luv 9090
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


### dig

Find IP mapped to DNS record (by geting `A` records for specified `Domain Name`)
```
dig ukr.net

    ; <<>> DiG 9.10.6 <<>> ukr.net
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 28419
    ;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags:; udp: 512
    ;; QUESTION SECTION:
    ;ukr.net.			IN	A

    ;; ANSWER SECTION:
    ukr.net.		121	IN	A	104.18.9.128
    ukr.net.		121	IN	A	104.18.8.128

    ;; Query time: 147 msec
    ;; SERVER: 192.168.149.132#53(192.168.149.132)
    ;; WHEN: Thu Mar 17 16:55:26 EET 2022
    ;; MSG SIZE  rcvd: 68
```

Get `MX` records for specified `Domain Name`
```
dig -t mx ukr.net

    ; <<>> DiG 9.10.6 <<>> -t mx ukr.net
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 10984
    ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags:; udp: 512
    ;; QUESTION SECTION:
    ;ukr.net.			IN	MX

    ;; ANSWER SECTION:
    ukr.net.		1116	IN	MX	10 mxs.ukr.net.

    ;; Query time: 159 msec
    ;; SERVER: 192.168.149.132#53(192.168.149.132)
    ;; WHEN: Thu Mar 17 16:59:33 EET 2022
    ;; MSG SIZE  rcvd: 56
```

#### dig: DNS forward quering demonstration

Let's resolve IP for `www.example.com` as an example of recursive DNS quering process.

> **NOTE**: With help of `dig @<NS> <DNS_NAME>` we can ask specific `Namespace Server` to resolve necessary DNS name

**Step 1**: Ask one of [Root Servers](https://www.iana.org/domains/root/servers) about `www.example.com`
```
dig @a.root-servers.net www.example.com

  ...
  ;; AUTHORITY SECTION:
  com.			172800	IN	NS	e.gtld-servers.net.
  com.			172800	IN	NS	b.gtld-servers.net.
  com.			172800	IN	NS	j.gtld-servers.net.
  ...
```
It doesn't provide IP for `www.example.com`, but it provides info where to find `NS` for `.com` domain


**Step 2**: Ask one of provided `NS` for `.com` domain about `www.example.com`
```
dig @e.gtld-servers.net. www.example.com

  ...
  ;; AUTHORITY SECTION:
  example.com.		172800	IN	NS	a.iana-servers.net.
  example.com.		172800	IN	NS	b.iana-servers.net.
  ...
```
It doesn't provide IP for `www.example.com`, but it provides info where to find `NS` for `example.com` domain


**Step 3**: Ask one of provided `NS` for `example.com` domain about `www.example.com`
```
dig @a.iana-servers.net. www.example.com

  ...
  ;; ANSWER SECTION:
  www.example.com.	86400	IN	A	93.184.216.34
  ...
```
The `NS` of this level knows IP for necessary website, so resolves it.



#### dig: DNS reverse lookup quering demonstration

Lets take a look for the `128.230.18.198`:

> **NOTE**: Only if the reverse lookup zone has been set up properly.

**Step 1**: Ask root `NS` whether it knows about `128.230.18.63` IP.
> **NOTE**: Pay attention at `QUESTION SECTION` section.
> It shows that necessary IP was reversed and completed with `in-addr.arpa` part,
> so actual search is done for `63.18.230.128.in-addr.arpa` DNS name.
```
dig @a.root-servers.net -x 128.230.18.63

  ...
  ;; OPT PSEUDOSECTION:
  ; EDNS: version: 0, flags:; udp: 4096
  ;; QUESTION SECTION:
  ;63.18.230.128.in-addr.arpa.	IN	PTR

  ;; AUTHORITY SECTION:
  in-addr.arpa.		172800	IN	NS	e.in-addr-servers.arpa.
  in-addr.arpa.		172800	IN	NS	f.in-addr-servers.arpa.
  in-addr.arpa.		172800	IN	NS	d.in-addr-servers.arpa.
  ...
```
Root `NS` doesn't know about `63.18.230.128.in-addr.arpa` DNS name, but suggests to ask `in-addr.arpa` `NS`.

**Step 2**: Ask `in-addr.arpa` `NS` regarding necessary IP.
```
dig @e.in-addr-servers.arpa. -x 128.230.18.63
  ...
  ;; AUTHORITY SECTION:
  128.in-addr.arpa.	86400	IN	NS	arin.authdns.ripe.net.
  128.in-addr.arpa.	86400	IN	NS	z.arin.net.
  128.in-addr.arpa.	86400	IN	NS	y.arin.net.
  128.in-addr.arpa.	86400	IN	NS	r.arin.net.
  ...
```
It doesn't know regarding `63.18.230.128.in-addr.arpa` DNS name, but suggests to ask `128.in-addr.arpa` `NS`.


**Step 3**: Ask `128.in-addr.arpa` `NS` regarding necessary IP.
```
dig @arin.authdns.ripe.net -x 128.230.18.63
  ...
  ;; AUTHORITY SECTION:
  230.128.in-addr.arpa.	86400	IN	NS	ns1.syr.edu.
  230.128.in-addr.arpa.	86400	IN	NS	ns2.syr.edu.
  ...
```
It doesn't know regarding `63.18.230.128.in-addr.arpa` DNS name, but suggests to ask `230.128.in-addr.arpa` `NS`.

**Step 4**: Ask `230.128.in-addr.arpa` `NS` regarding necessary IP.
```
dig @ns1.syr.edu -x 128.230.18.63
  ...
  ;; ANSWER SECTION:
  63.18.230.128.in-addr.arpa. 60	IN	PTR	syr-prod-web.syracuse.edu.
  63.18.230.128.in-addr.arpa. 60	IN	PTR	syr-prod-web1.syr.edu.
  63.18.230.128.in-addr.arpa. 60	IN	PTR	syr.edu.
  ...
```
This `NS` knows necessary IP, so replies correspondig DNS record via `PTR` record type.





## Scan Remote Server to find: open ports, OS, etc

### nmap (network map)

Use `nmap` tool
```
nmap -sS -O <IP_of_remote_server>
```

### zenmap
Same as `nmap`, but with UI.





## Connections

### nc

> NOTE: `nc` (aka `netcat`) is a computer networking utility for reading from and writing to network connections using `TCP` or `UDP`.

Available options
```
# MacOS
nc -help
```

Act like a server (listen port `9090` for inbound `UDP` connections)
```
# MacOS
nc -luv 9090
```


Act like a client (send data to port `9090` via `UDP` connection)
```
# MacOS
# nc -u <DEST_IP> <DEST_PORT>
nc -u 10.0.2.7 9090
```


## Autonomous Systems, BGP


### ripe.net

There some collectors that collect corresponding data.

This website provides visualisation of such data.

Here we can see:
- [AS Neighbors](https://stat.ripe.net/widget/asn-neighbours)
- [What Prefix was announced for the AS](https://stat.ripe.net/widget/announced-prefixes)
- [What AS Path was announced for the specific Network Prefix](https://stat.ripe.net/widget/looking-glass)
- [Visualize AS path](https://stat.ripe.net/widget/bgplay)



### Tools

In which `AS` specified `IP` address is located.
```
whois -h whois.radb.net 31.13.78.3
```

Which `IP` prefixes contain specified `AS`
```
whois -h whois.radb.net -- '-i origin AS32934' | grep route:
```



















