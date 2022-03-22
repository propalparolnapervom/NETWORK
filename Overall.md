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


## Layer 2: Data Link Layer

Sender `A` needs to send a data to Receiver `B`.

`A` and `B` are located on different local networks, connected by the Internet.

What the data flow?

### MAC Header 

> **NOTE**: `MAC Header` is a general name, it's also called `Ethernet Header` in case if Ethernet is in use.

> **NOTE**: Within a local network, communication happens only via `MAC Address`.

`A` constructs an `IP packet` which consist of:
   1) payload (in this case, data itself);
   2) IP header:
   - source IP address (`A`);
   - destination IP address (`B`).

The `IP packet` can not be send from `A` to `B` directly, as they are not at the same local network. Thus, not connected to the same physical wire, for example.

Thus, `Routers` should be involved to provide this communication, as they physically present simultaneously in 2 or more local networks and know how to route traffic between them. 

Thus, to send `IP packet` outside of network, it should be send by `A` to the router inside of its local network. Let it be `R1`.

In order to do that, additional header of `Layer 2` is added to the `IP packet` by `A`:

   3) MAC header:
   - source MAC address (`A`);
   - destination MAC address (`R1` router);
   - type of payload (`IP packet` or `ARP packet`).

Now it is called a `Frame` (as this is a name for a data on `Layer 2`).

This `Frame` is sent by `A` as a broadcast message to all receivers in the local network. Network Interface Card of every receiver in the local network looks at the destination `MAC Adress` with a question "Is it for me?":
   - if no, the `Frame` is dropped;
   - if yes, the `Frame` is taken into the work (provided to the upper `Layer 3`, ..., up to `Application Layer 7`).

So `R1` receives such broadcast message (because its `MAC Adress` specified as a destionation `MAC Adress`). Then:
   - removes old `MAC Header`, added by `A`;
   - looks at the `IP packet`;
   - founds out that this is `IP A` -> `IP B` communication.

As router `R1` knows how to route traffic to the necessary `B`, it sensds it to the `R2` router.

In order to do that, it adds to the original `IP packet` additional header of `Layer 2`.

Its done at the same exact way as it was done by `A`, but with new source/destination MAC adresses:

   3) MAC header:
   - source MAC address (`R1` router);
   - destination MAC address (`R1` router);
   - type of payload (`IP packet` or `ARP packet`).

Such removing old `MAC Header`, looking at `IP` adresses, adding new `MAC Header`  will be done multiple times by multiple routers within an Internet.

Eventually, `Rk` router will be reached, which is located within the same local network as `B` (thus, directly connected to `B`).

`Rk` removes `MAC Header` too, looks that this is `IP A` -> `IP B` communication. And as it knows where `B` is located, the following is done at the same exact way as it was done multiple times before: a new `MAC Header` is added to the original `IP packet`, but with new source/destination MAC adresses:

   3) MAC header:
   - source MAC address (`Rk` router);
   - destination MAC address (`R1` router);
   - type of payload (`IP packet` or `ARP packet`).

This `Frame` arrives to the destination `B`. 

Then `B` removes `MAC Adress` header, looks that destination `IP B` is his `IP`, so processes the packet (provides to the upper `Layer 3`, ..., up to `Application Layer 7`).

That's how packet from `A` arrives to `B`.

> NOTE: The analogy.
> `IP packet` is you, `Frame` (so `IP packet` + `MAC Header`) is the bus.
> So packet traveling from `A` to `B` is like you, traveling on the multiple buses from `A` to `B`. 
> You change the bus to the new one every time you arrive to a new router.
> Every bus has its own source and destination point.



### ARP




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












