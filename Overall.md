# Documentation

[Udemy: Internet Security](https://www.udemy.com/course/du-internet-security)


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
  - time exceeded


### ICMP: Error Message "time exceeded"

The messages have `11` in the `Type` field of `ICMP Header`.


Possible reasons:
- TTL became 0 and router had to drop the packet;
- IP fragmentation was involved, but original packet couldn't be assembled (some new packet were lost eventually);



### ICMP: Error Message "destination unrecheable"

The messages have `3` in the `Type` field of `ICMP Header`.

The messages have following in the `Code` field of `ICMP Header` (subtype of the main type).

| Code | Reason |
| ---- | ------ |
| 0 | Destination **network** unrecheable |
| 1 | Destination **host** unrecheable |
| 2 | Destination **protocol** unrecheable |
| 3 | Destination **port** unrecheable |
| 4 | Fragmentation required, but DF flag is set |



### ICMP: Control Message "echo request/reply"

This type of ICMP messages is used by `ping` tool:
- `sender` sends ICMP message:
  - with `8` in the `Type` field of `ICMP Header`;
  - with some data in the `Data` field of `ICMP Header`;
  - this is called a **request**.
- once `receiver` gets this message, on its `Layer 3: Network` it:
  - understands that this is a request message;
  - sends back ICMP message, which is called **reply**;
  - with `0` in the `Type` field of `ICMP Header`;
  - with some data in the `Data` field of `ICMP Header`;

If the data in reply is the same as in request:
- the receiver is alive;
- the connection is OK. 

That's why it's called **echo**.



### ICMP: Control Message "redirect"

The messages have `5` in the `Type` field of `ICMP Header`.

The messages have following in the `Code` field of `ICMP Header` (subtype of the main type).

| Code | Reason |
| ---- | ------ |
| 0 | Redirect for **network** |
| 1 | Redirect for **host** |


#### Purpose of redirect ICMP control message

A local network has:
- 2 routers: `R1` and `R2`;
- computer `A`.

Another local network has:
- computer `B`.

`A` -> `B` communication should be done.

Usually, the best way to do that is to route traffic via `R1`. So `A` has corresponding item in its route table:
- to reach `B`, use `R1`.

Then something changed within a network, and `R1` realized that `R2` would be the best choice now. But `A` still has old item in its route table.

So `R1` still gets trafic from `A`, but now it redirects it to `R2`.

For such situation, `R1` can send redirect ICMP control message to `A` with a suggestion to update its route table to the more optimal one:
- to reach `B`, use `R2`.

Thus, next time `A` sends traffic to `B`, it will use `R2`.

> **NOTE**: No security is involved into this protocol. But seems like, for example, OS Ubuntu has `net.ipv4.conf.all.accept_redirects=0` by default, which doesn't allow to accept such ICMP redirect messages from security p.o.v 

> **NOTE**: You can redirect TO **only** machines within your local network.

> **NOTE**: You can send redirect messages **only** FROM machines within your local network.



# Layer 4: Transport

## Transport Layer: Purpose


### Analogy

There is a company with many departments: IT, finance, operations, etc. 

I work in the company in IT department.

Some sender sends a letter to me.

The postman delivers the letter to the company's reception desk. And girl from a repeption desk then somehow delivers letter to specific department within a company (me, in IT department in this case).

> **NOTE**: How to deliver letter from sender to the company's reception desk - `Layer 3: Network`.
>           How to deliver letter further from company's reception desk to me in IT department - `Layer 4: Transport`

If letter was lost during delivery to company's reception desk - `Layer 3: Network` doesn't do anything. `TCP` from `Layer 4: Transport` will try to re-send lost packet and make a correct order (if it was broken).


### Port

To specify, which exact department within a company is a receiver (which exactly App on the computer), `Layer 4: Transport` provides additional info: `Port`.

> **NOTE**: Application that waits for the packet, must let OS know that it will register for the `Port` number. So once a letter arrives to the reception desk with this `Port` specified, it should be delivered to the Application.

`Socket` is a window between `App` and `OS Kernel`. `App` has to bind a `Socket` with some `Port` number. Thus `OS` knows that the `Port` number is registered by `App`.

Thus, once packet is arrived with specified `Port` number as a destination, `OS` knows that it should:
- put the packet to the buffer;
- wake up necessary `App`, that is registered for the corresponding `Socket`, to let `App` read the packet from the buffer.

## Protocols

|                 | TCP  | UDP    |
| ----------------| ---- | ------ |
| Connection      |  Y   |    N    |
| Packet boundary |  packet is removed, only data from inside is provided to App    |   data provided to App together with packet     |
| Reliability      |   Y   |   N     |
| Ordering      |   Y    |    N    |
| Speed      |   N   |    Y    |
| Broadcast      |  N    |   Y     |

## UDP Protocol

The most important info, that is added within `UDP Header` (in addition to lower `IP Layer`):
- source `Port` number;
- destination `Port` number.

UDP Applications:
- DNS Protocol
  - NOTE: But it uses `TCP` as well;
- video/audio streaming, skype, zoom
  - NOTE: Netflix, YouTube use `TCP` (because it's not real-time and can wait to load data);
- real-time applications;
- VPN Tunnel (OpenVPN).

> **NOTE**: `UDP` doesn't support packets ordering (if it arrives in wrong order) and doesn't handle packets lost. `TCP` does. 
> What if ordering and loss handling is cruical for you, but you don't want to use `TCP`?
> In this case you have to handle ordering and packet lost on `App` level by yourselve.


## TCP Protocol

### TCP: purpose

Virtual connection between `A` and `B`:
  - once `TCP` connection is established, `A` and `B` can consider there's a "pipe" between them;
  - actually, there's 2 pipes: `A`->`B` and `B`->`A`;
  - once packet on the one end of the pipe, it will be on the other one;
  - the "pipe" is not real (like physical connection during old calls by phone via multiple switches), it's virtual: there's a software swithes instead of physical ones;


With help of such pipe, unlike `UDP`, `TCP` provides:
- ordering of packets:
  - 2nd packet might arrive before 1st packet, but it will be delivered to the `App` only in the correct order (1st, then 2nd);
- reliability:
  - if packet is lost, `TCP` has ability to detect this and re-transmit the packet;
  - of course, the re-transmition might be also failed, but at least there's an attempt;
- flow control:
  - `A` might be much faster, then `B` can proceed;
  - `B` in this case will be overwelmed;
  - `TCP` provides a mechanism to control the flow speed to avoid this;
  - also, there could be a conjustion somewhere between `A` and `B` on the Internet, and `TCP` can slow down the flow to avoid it.

With help of `TCP`, a "virtual connection" is created, when `A` and `B` connected with some kind of virtual pipe.




### TCP: Buffers

So when `TCP` connection is established betwen `A` and `B`, 2 virtual pipes are created:
- `A`->`B`
- `B`->`A`

Actually, a buffers are created on both sides:
- for `A`->`B` pipe:
  - `A` writes to the `send buffer` on its side;
  - `B` reads from the `receive buffer` on its side;
- for `B`->`A` pipe:
  - `B` writes to the `send buffer` on its side;
  - `A` reads from the `receive buffer` on its side;

Overall, 4 buffers: 
- send/write on `A`;
- send/write on `B`.

Both pipes act at the same manner. The only difference is a direction.

> **NOTE**: `TCP` doesn't send data immidiately. It does some internal optimization to decie when to send the data. Before sending, data is in the buffer.

#### Sender side

Sender **writes** some data to the `sender buffer`.

`TCP` uses following criterias to decide when to **send** the data:
- timing:
  - `App` can write to a `send buffer` 1 byte at a time;
  - to send each packet, you need to add `TCP` header and `IP` header - so 1 byte data will consume a lot of effort;
  - so prior to send data from `send buffer`, `TCP` waits for some time (typically ~200ms) to see if new data will arrive;
- we already have data of `MTU` size:
  - when data in buffer has been kept less then ~200ms, but the size of data is alredy reached Maximum Transmition Unit size, it will be sent;
  - (if you waited longer and created a packet bigger then MTU size, it'd be needed to make `IP fragmentation` as we can not send data bigger, then `MTU` - and that's consumes more effort, so should be avoided)


#### Receiver side

Some data arrived to the `receiver buffer`. Let's assume, it's in 1st, 2nd and 4th packets.

`TCP` will:
- deliver data from `1st` and `2nd` packets to the `App`;
- not deliver data from `4th` packet for a while (as `3rd` packet is lost);
- wait for the `3rd` packet for some time;
- if no `3rd` packet arrived after some time, drop `4th` packet (as there's a gap).

So `TCP` is aimed to deliver data at the same order it was sent by sender.

> **NOTE**: `TCP` will decide, when to wake up the `App` in order to read data from the `receiver buffer`. It's not necessary just after packet arrives to the buffer. It depends on some timeline and the amount of data within the `receiver buffer`.



### TCP: Order and Reliability

Each byte in the `sender buffer` has a sequence number.

When `TCP` decides its time to send data from `sender buffer`, it gets some amount of bytes and forms a packet.

The packet has `seq #` field in the header, which is a sequence number of the 1st byte in the packet.

Thus, when a packets arrive to the `receiver buffer`, they put in right order.

When its time to provide data from packets to the `App`, it will be done only for packets without gaps in the order.

For example, if packets #1 and #3 have arrived, its clear that packet #2 is not in the buffer so far.

The data will be provided from packet #1, and then stoped. Even if we have packet #3. Next portion of data will be provided only after packet #2 arrives.

Receiver sends `ACK` message, where it says: next expected sequence is #2. Sender then tries to re-send this sequence.

Once a Sender gets `ACK` message with some sequence #, it knows that everything prior to the sequence # was arrived successfully.



### TCP: Flow and Congestion Control

Situations could be:
- `A` can send data much faster then `B` can consume the data;
- `A` sends data to `B` with normal pace, but there is a congestion on some of the routers within an Internet;

To avoid such situations, there `TCP` uses a `sliding window` on a `sender buffer`: starts at `seq #X`, ends on `seq #Y`.

> **NOTE**: Within `sliding window`, Sender can send data as fast as it can, without waiting for `ACK` messages from a Receiver.

Once sender got `ACK` message (for `seq #Z`, for example), it moves start point of `sliding window` accordingly (so now it starts from `seq #Z`).

The length of `sliding window` is changing dynamically:
- depending on Receiver capacity:
  - when Receiver realizes only 100 bytes left within its `receiver buffer`, it sends to Sender a `window advertising message` that 100bytes is a maximum it can get;
  - sender then makes length of its `sliding window` no more then one, specified in `window advertising message` (so, 100bytes in this example);
  - if a `window adevtising message` says 0 bytes left on Receiver side, Sender shrinks its `sliding window` to 0 - so no new data will be send at all;
- depending on traffic on the route between Sender and Receiver:
  - there could be a congestion at some of the routers within an Internet, when router is so busy, it can't handle new packets, so it drops new packets;
  - as packets dropped, receiver didn't get it, so no `ACK` messages sent to the sender, so sender realizes something went wrong on the route;
  - sender knows that if he keeps send packets with the same pace, situation can get worth;
  - thus, sender shrinks `sliding window` to speed down packets sending process;

> **NOTE**: It would be a constant congestion in the Internet, if all senders sent its packets with no such aggastments regarding congestions.


## TCP Header

It contains fields to provide information, needed for a mechanism, described above. Including:
- src/dest ports;
- sequence number (of a first byte in the packet, added on the sender side);
- acknowledgment number (`ACK` bit has to be turned on) (added on receiver side to describe, from which sequence # the gap in `receiver buffer` starts);
- window size (`window advertising message` - how many bytes are left within a `receiver buffer`);
- urgent pointer (`URG` bit has to be turned on) (within a `data` field, the end of the first bytes, that are considered as urgent - so need to be read first; data after that pointer is considered as normal data);
- bits to be turned on or off:
  - URG
  - ACK
  - PSH
  - RST
  - SYN
  - FIN


## TCP Connections Handling

### TCP: Establish Connection (TCP Handshake)

`A` ----> `B`
- **SYN** bit turned on (to init conn for this direction);
- **sequence number** field set to **X** (random number for this direction);

`A` <---- `B`
- **ACK** bit turned on (to show that init request was received from `A`);
- **acknowledgment number** field set to **X+1** (to show that init number X was received from `A`, it will be sent back after set +1);
- **SYN** bit turned on (to init conn for this direction);
- **sequence number** field set to **Y** (random number for this direction);

`A` ----> `B`
- **ACK** bit turned on (to show that reply was received from `B`);
- **acknowledgment number** field set to **Y+1** (to show that number Y was received from `B`, it will be sent back after set +1);
- **sequence number** field set to **X+1** (??? to show that **ACK** message from `B` was received succesfully ???);

Once the handshake is done, the buffers will be created specifically for this `TCP` connection:
- on the `A` side:
  - `sender buffer`
  - `receiver buffer`
- on the `B` side:
  - `sender buffer`
  - `receiver buffer`


### TCP: Finish Connection (Normal)

Connection between `A` and `B` is bi-directional. So it has to be finished one by one: one direction, then second direction.

Finishing one direction:
- `A` ----> `B`
  - **FIN** bit turned on (to init conn finishing for this direction);
  - **sequence number** field set to **X** (whatever sequence number was for the buffer for this direction);
- `A` <---- `B`
  - **ACK** bit turned on (to acknowlege that init conn finishing was received for this direction);
  - **acknowlege number** field set to **X+1** (to show that init number X was received from `A`, it will be sent back after set +1);

Finishing other direction:
- `A` <---- `B`
  - **FIN** bit turned on (to init conn finishing for this direction);
  - **sequence number** field set to **Y** (whatever sequence number was for the buffer for this direction);
- `A` ----> `B`
  - **ACK** bit turned on (to acknowlege that init conn finishing was received for this direction);
  - **acknowlege number** field set to **Y+1** (to show that init number X was received from `A`, it will be sent back after set +1);





## TCP vs UDP: boundaries between messages

So we have 2 separate messages to be sent:
- "Hello, world"
- "Hello, Universe"

Will receiver know, where is the boundary between those messages? (where 1st one is finished and 2nd is started)

### Boundaries: UDP

Each message is sent as a packet.

Receiver gets each packet separately.

So in case of `UDP` its clear for the receiver, where is 1st message and where its 2nd one.

### Boundaries: TCP

Both messages are:
- written to the `sender buffer` on the sender side;
- at some point in time some of the packets send over the network;
- written to the `receiver buffer` on the receiver side;
- at some pint in time data from some packets in buffer is delivered to the `App`.

So in case of `TCP` it is not clear the boundary between such 2 messages, from the box.

But you can handle it by yourselve. For example, by sending number of bytes to read from buffer for each message (something like "5 hello 6 world", so read from buffer 5 bytes, which will be "hello", then read 6 bytes which will be "world")


## TCP vs UDP: hangling messages in the receiver buffer

There's machine `A` and machine `B`.

There 2 client on the machine `A`:
- client `1` on port `50000`;
- client `2` on port `60000`.

There 1 server on the machine `B`:
- server `S` on port `37`.


If clients `1` and `2` both send messages (from the same machine `A`) to the server `S` (on machine `B`), will those messages be merged within the same `receiver buffer`?

### Handling messages in receiver buffer: UDP

All messages from `1` and `2` will be placed in one `receiver buffer`.

But it's not a problem, as for `UDP` each message will be send as a separate packet.

So yes, receiver will read all those packets from one buffer, but it will distinct easily, who was a sender, with no data merged.


### Handling messages in receiver buffer: TCP

Each `A` to `B` connection creates its own "virtual connection" (with 2 pipes).

So even if `1` and `2` will send messages from the same machine, their port on the machine are different.

The following connections are created in such case:
- `IP A`:`Port 50000` <-> `IP B`:`Port 37` (consists of 2 corresponding pipes)
- `IP A`:`Port 60000` <-> `IP B`:`Port 37` (consists of 2 corresponding pipes)

For each client on the server will be:
- separate `TCP` connection;
- thus, separate "virtual pipe";
- thus, separate `receiver buffer`

So, messages from different clients on the same server will not be placed into the same `receiver buffer`. Separate buffer will be created for each client instead.




























