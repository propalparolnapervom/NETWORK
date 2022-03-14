## IP addressing


### Assigning IP Addresses

The following 4 components of fully configured client should be assigned `statically` (manually) or dynamicly (by DHCP server):
- IP adress
- subnet mask
- default gateway (usually, IP of your router)
- server adresses for DNS or Windows Internet Name Service (WINS) (Converts NetBIOS computer name into an IP address)


## Routing

The fundamentals:
- Traffic is routed to flow between subnets
- Each subnet is its own broadcast domain
- Routers are the layer 3 devices that separate broadcast domains, but multilayer
switches can also separate broadcast domains


### Routing Tables

Routing Decisions:
- Layer 3 to Layer 2 Mapping
     - Routers use `ARP caches` to map an `IP address` to a given `MAC address`
- Make packet-forwarding decisions based on its internal routing tables

Sources of Routing Information
- Directly Connected Routes (Learned by physical connection between routers)
- Static Routes (1) Manually configured by an administrator 2) Default static route (0.0.0.0/0) is a special case: “If I don’t know where, then send out default static route.”)
- Dynamic Routing Protocols (Learned by exchanging information between routers via corresponding protocols)


### Routing Protocols

Internal and Exterior Routing Protocols
▪ Interior Gateway Protocols (IGP)
● Operate within an autonomous system
▪ Exterior Gateway Protocols (EGP)
● Operated between autonomous systems












