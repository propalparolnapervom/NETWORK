## Overall

### How Application sends data over network?
OS kernel knows how to:
   - create a Package to be send over the network;
   - send it over the network.
     
Package constructions is done inside of `OS kernel`.

So `Application` doesn't need to know that. Instead, it should know how to provide necessary data to OS kernel.

`Application` communicates with `OS kernel` via `Socket API` (this is some kind of window for a communication between them).

`Application` provides following info to the `OS kernel`, via `Socket API`:
   - data itself, which has to be send;
   - `Transport Layer 4` info:
     - which protocol to use (`UPD` or `TCP`);
     - what is Destination `Port` number;
   - `Network Layer 3` info:
     - which protocol to use (`IPv4` or `IPv6`);
     - what is Destination `IP` adress;

    
Once data provided, `OS kerne`l then packages it in necessary form and sends it over the network.


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












