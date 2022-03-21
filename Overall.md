## How App communicate over network?

### How App sends data
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

    
Once data provided, `OS kernel` packages it into necessary form and sends it over the network.


### How App receives data

> NOTE: When you open the `Socket` at `OS` level, you must bind it to:
>          - `IP` adress - as server can have multiple `network interface cards`, so multiple `IP` adresses. and `App` can listen all of them or just specified ones; you define it via such bind;
>          - `Port` number - thus `OS` knows to which `App` give received package;


At `OS` level:
   - ... previous OSI layers are ommited here to simplify explanation ...
   - `Network Layer 3`:
     - looks if destination IP is the IP of current machine;
     - drops the package, if not;
   - `Transport Layer 4`:
     - looks which transport protocol was used (`UDP` or `TCP` or ...);
     - moves package to corresponding OS module (`UDP` OS module to work with `UDP`, for instance);
     - `UDP` OS module looks which destination Port number was specified in the package;
     - Inside the `OS`, the `App` and `Port` number are mapped. So when package arrives, `Transport Layer` knows, which `App` should receive the data;
     - So once the package is received, it moved to a `Buffer`, mapped to the `Port`

At `App` level:
   - once the package in the `Buffer`, the `App` can read it;
   - it can be that `App` is always blocked when there is no data; in this case `OS` wakes `App` up, once the packages are in the buffer;

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












