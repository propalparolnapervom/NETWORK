# How App communicates over the network?

## How App sends data
OS kernel knows how to:
- create a Package to be send over the network;
- send it over the network by making routing decision:
  - chosing, whether it's local network or router has to be used;
  - which router to use in the local network (if there are few of them);
  - which Network Interface Card to use (if the computer has multiple of them);
     
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

    
Once data provided, `OS kernel` packages it into necessary form:
- on `Layer 4: Transport` it creates `Segment`: adds `UDP` (or `TCP`) header to payload from previuos step (so, data itself from App);
- on `Layer 3: Network` it creates `IP packet`: adds `IP` header to payload from previuos step (so, `Segment`);
- on `Layer 2: Data Link` it creates `Frame`: adds `MAC` header to payload from previuos step (so, `IP packet`);

Then `OS kernel` makes routing decision:
- choses which router to use (if many);
- choses which network interface card to use (if many).

Then `OS kernel` sends the package.



## How App receives data

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


> **NOTE**: See corresponding block below to get more info on processes that are going on on each separate OSI layers.


# Layer 2: Data Link

Sender `A` needs to send a data to Receiver `B`.

`A` and `B` are located on different local networks, connected by the Internet.

What the data flow?

## MAC Header 

> **NOTE**: `MAC Header` is a general name, it's also called `Ethernet Header` in case if Ethernet is in use.

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

> **ANALOGY**
>
> `IP packet` is you, `Frame` (so `IP packet` + `MAC Header`) is the bus.
> So packet traveling from `A` to `B` is like you, traveling on the multiple buses from `A` to `B`. 
> You change the bus to the new one every time you arrive to a new router.
> Every bus has its own source and destination point.


## ARP

> **NOTE**: `ARP` is for Adress Resolution Protocol.

> **NOTE**: This is a `Layer 2` protocol, as it works with `MAC Adresses`.

Within a local network (so when 2 computers are on the same cable, for example), communication happens only via `MAC Address`. Even if `IP` is known.

That's because `Network Interface Card` doesn't look at `IP`, it looks at `MAC Adress` within a `MAC Header` of a `Frame`.

> `ARP` protocol is responsible for getting `MAC Adress` for given `IP Adress` of receiver.


> **ANALOGY**
>
> In the room few people. You know that on of them is Bob, but you don't know who exactly.
> So you loudly (thus, all people in the room can here you) ask: "Who is Bob?"
> Once Bob heard you, he raises his hand.
> All other people heard you too, but they didn't respond, as no one is Bob among them.
> 
> Bob is `IP`, room is local network. Calling is `ARP request`, Bob raising the hand is `ARP responce`.


Sender sends `ARP request` packet (as a **broadcast**, as receiver is unknown by its `MAC adress` yet) with (among other info):
- sender info (fully known):
   - MAC adress (known);
   - IP adress (known);
- target info (partially known):
   - MAC adress field is empty (not known, trying to get this knowledge);
   - IP adress (known).

Receiver (which is on the same local network) sends `ARP responce` packet (as a **unicast**, as this time sender knows target by its `MAC adress` already) with (among other info):
- sender info - now its info for target machine (fully known):
   - MAC adress (known);
   - IP adress (known);
- target info - now its info of the original sender (fully known):
   - MAC adress (known);
   - IP adress (known);

> **NOTE**: Once this initial request/responce communication is finished, destination `MAC Adress` is known to sender.
> This `IP`->`MAC` mapping is saved then to the `ARP cache` for a while, to do not do such communication each time a packet should be send.

`ARP` protocol is low-level (`Layer 2`) protocol, thus, in order to be very efficient in terms of perfomance, it has to be very simple:
- no encryption;
- no error detection;
- etc

Also, it is stateless: once request is sent, sender doesn't remember that it was sent. So once responce is get, it will update `ARP cache`.







# Layer 3: Network

## IP protocol

Basic functions:
- at network:
  - routing
- at OS:
  - passing packets to the upper layer (`Layer 4: Transport`)
  - providing error detections and diagnostic capability.

> NOTE: It's not responsible for reliable transmition (if later packet comes before earlier packets, for example) (`TCP` from `Layer 4` is in charge of that).
> This is "best effort delivery": it tries its best to make a packet delivery, but if something is happening during delivery - nothing will be done to fix it.


## Assigning of IP Addresses

The following 4 components of fully configured client should be assigned `statically` (manually) or dynamicly (by DHCP server):
- IP adress
- subnet mask
- default gateway (usually, IP of your router)
- server adresses for DNS or Windows Internet Name Service (WINS) (Converts NetBIOS computer name into an IP address)


## IP fragmentation

When `OS kernel` constructs the `Frame`, which is `MAC Header` + payload (`IP packet`), it has a limit for a payload length:
- no less then `46 bytes` - this size is big enough to let sender time to detect a collision at the local network (if any); so if receiver gets payload with size less then this one, it's considered as corrapted one;
- no more then `1500 bytes` - physical limitation of the Ethernet, for example.

Upper limit is also called `MTU` - Maximum Transmittion Unit. It can be set: 
- on the machine of sender, so during initial packet creation no more then `1500 bytes` can be added to payload;
- on the router during packet transmittion over the network (at this point MTU can be even smaller then the one, set up on the initial machine of sender).

Each time package is bigger, then `MTU` (on sender's machine or router), the packet has to be divided on smaller packets, which might be routed to the receiver via different routes.

Eventually it will be assembled back to the packet of the original size on the receiver side: at the `OS kernel`, at `IP layer`.

If some packets are losted, the packet is considered as corrupted one, and eventually dropped.

`IP fragmentation` field is used at the `IP Header` of the packet to track information about such packet divisions: which smaller packet is 1st, 2nd, etc.



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
- Static Routes:
  - Manually configured by an administrator
  - Default static route (0.0.0.0/0) is a special case: “If I don’t know where, then send out default static route.”)
- Dynamic Routing Protocols (Learned by exchanging information between routers via corresponding protocols)

Routing tables are configured:
- for the `Router`:
  - routing protocols;
  - attacks on the routing protocols (`BGP`, for example);
- for the `Host`:
  - DHCP
  - default routers
  - manual configuration
  - ICMP redirect messages



### Routing Protocols


Internal and Exterior Routing Protocols
- Interior Gateway Protocols (IGP) - Operate **within** an autonomous system
- Exterior Gateway Protocols (EGP) - Operated **between** autonomous systems

Dynamic Routing Protocols:
- More than one route can exist for a network
- Different protocols consider different criteria when deciding which route to give preference
- Based on number of hops (hop count in `RIP`), link bandwidths (`OSPF`), or other criteria



| Routing Protocol | Abbreviation | Type | Interior/Exterior |
| ---------------- | ------------ | ----- | ----------------- |
| Routing Information Protocol | RIP | Distance vector | Interior |
| Open Shortest Path First | OSPF | Link state | Interior |
| Enhanced Interior Gateway Routing Protocol | EIGRP | Advanced distance vector | Interior |
| Intermidiate System-to-Intermidiate System | IS-IS | Link state | Interior |
| Border Gateway Protocol | BGP | Path vector | Exterior |


## ICMP protocol

> **NOTE**: `ICMP` stands for Internet Control Message Protocol


ICMP itself uses IP.

ICMP is used for:
- Control Messages - when you want to exchange info, but only on `Layer 3` level:
  - echo request/reply
  - redirect;
  - timestamp request/reply;
  - router advertisement/solicitation
- Error Messages - if I drop a message, I need to send an error message back to the sender:
  - destination is unreacheble
  - time exceeded:
    - TTL became 0 and router had to drop the packet;
    - IP fragmentation was involved, but original packet couldn't be assembled



### ICMP: echo request/reply

This type of ICMP messages is used by `ping` tool:
- `sender` sends ICMP message:
  - with `8` in the `Type` field;
  - with some data in the `Data` field;
  - this is called a **request**.
- once `receiver` gets this message, on its `Layer 3: Network` it:
  - understands that this is a request message;
  - sends back ICMP message, which is called **reply**;
  - with `0` in the `Type` field;
  - with some data in the `Data` field;

If the data in reply is the same as in request, the connection is OK. That's why it's called **echo**.











