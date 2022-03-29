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

To establish `TCP` connection between `A` and `B`, a handshake from 3 steps should be done.

`Step 1`: `A` ----> `B`
- **SYN** bit turned on (to init conn for this direction);
- **sequence number** field set to **X** (random number for this direction);

`Step 2: `A` <---- `B`
- **ACK** bit turned on (to show that init request was received from `A`);
- **acknowledgment number** field set to **X+1** (to show that init number X was received from `A`, it will be sent back after set +1);
- **SYN** bit turned on (to init conn for this direction);
- **sequence number** field set to **Y** (random number for this direction);

`Step 3`: `A` ----> `B`
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

`App` wants to finish communication, in a normal way. 

It closes a `Socket`, which triggers following steps.

> **NOTE**: Connection between `A` and `B` is bi-directional. 
> So it has to be finished one by one in 2 steps: one direction, then second direction.

`Step 1`: Finishing one direction
- `A` ----> `B`
  - **FIN** bit turned on (to init conn finishing for this direction);
  - **sequence number** field set to **X** (whatever sequence number was for the buffer for this direction);
- `A` <---- `B`
  - **ACK** bit turned on (to acknowlege that init conn finishing was received for this direction);
  - **acknowlege number** field set to **X+1** (to show that init number X was received from `A`, it will be sent back after set +1);

`Step 2`: Finishing other direction (same steps, but from other side)
- `A` <---- `B`
  - **FIN** bit turned on (to init conn finishing for this direction);
  - **sequence number** field set to **Y** (whatever sequence number was for the buffer for this direction);
- `A` ----> `B`
  - **ACK** bit turned on (to acknowlege that init conn finishing was received for this direction);
  - **acknowlege number** field set to **Y+1** (to show that init number X was received from `A`, it will be sent back after set +1);

At this point both sides terminated its connections. `TCP` connection between `A` and `B` is no longer exist.


### TCP: Finish Connection (Abnormal)

When some abnormal situation happens, `TCP` connection can be terminated in abnormal way.

No bi-directional closing is present in this way. Only one side initiates a termination.

- `A` ----> `B`
  - **RST** bit turned on (to init conn finishing for whole connection);
  - **sequence number** field set to **X** (whatever sequence number was for the buffer for this direction);

> **NOTE**: In such case `B` would accept it only with **sequence number** field set correctly to **X** (together with other info: src/dst IP, src/dst Ports).

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



# Layer 4: Application


## DNS

### DNS: Zone vs Domain

`Zone` - a collection of the `Records` that is hosted on the `Name Server`.

If **whole** domain info is hosted on one `NS`, then `Zone` and `Domain` are equal: `Domain` has one `Zone`.

If domain is a big one, and you don't want to host all its information of single `NS`. Instead, you want to keep some of its subdomain on different `NS`: that's when `Domain` and `Zone` are different.

> NOTE: So:
> - `Zone` is associate with a `NS`;
> - `NS` could host many `Zones`;
> - each `Zone` represents a sub-domain;


`Zone File` - refers to the DB that is used by `NS` for the particular sub-domain.

### DNS: Hierarcy

DNS is too big to have it on one centrilized computer, so some hierarcy (categorization) to make it decentralized:
- [Root Servers](https://www.iana.org/domains/root/servers);
- TLD (Top Level Domain) Servers:
  - for `.com` domain;
  - for `.ua` domain;
  - etc
- next levels, if needed:
  - for `example.com`, for example;
  - for `museum.ua`, for example;
- next levels, if needed:
  - for `uk.example.com`, for example;
  - for `tickets.museum.ua`, for example;


### DNS: Query Process


DNS queiring is iterative process: if Local DNS server doesn't know the IP, it will ask each server from DNS hierarcy until he gets the answer.

So for `www.example.com` it would be like:
- `User Machine` --- [www.example.com] --->   `Local DNS server`

- `Local DNS Server`   --- [www.example.com] --->   `Root server`
- `Local DNS Server`   <--- [.com] ---              `Root server`

- `Local DNS Server`   --- [www.example.com] --->   `TLD server` for `.com`
- `Local DNS Server`   <--- [example.com] ---       `TLD server` for `.com`

- `Local DNS Server`   --- [www.example.com] --->   `Domain server` for `example.com`
- `Local DNS Server`   <--- [199.191.50.18] ---     `Domain server` for `example.com`

- `User Machine` <---[199.191.50.18]--- `Local DNS Server`


> **NOTE**: The `Local DNS Server` knows where to find IP of `Root server`, becase such cruical information  often is embedded into the software.
> For example, Ubuntu has `/etc/bind/named.conf.default-zones` file, which points to the `/etc/bind/db.root` file, where IPs for all 13 `Root servers` specified.

In other case, `Local DNS Server` wouldn't know how to resolve any DNS name, as it doesn't have other `Local DNS server`, but it must go to `Root server` instead.

> **NOTE**: The `Local DNS Server` is a historical name from times, when in order to get info as quickly as possible, the server was placed directly within your local network.
> Nowadays, it can be placed anywhere, even in the Interned. So, for example, Google's `NS` `8.8.8.8`, located in the Internet, can be specified by you as your `Local DNS Server`.


Let's resolve IP for `www.example.com` as an example of such recursive DNS quering process.

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



### DNS: What happens when you buy a Domain

For example, you have bought `xburser.com` domain from `GoDaddy`.

You have to add an info to corresponding TLD (`.com` in this case). When you buy the domain, `GoDaddy` makes the adding instead of you.




### DNS: Let User Machine know where Local DNS server is


> **NOTE**: This is for Linux.

The `User Machine` knows where to find IP of `Local DNS Server`, becase of information specified within `/etc/resolv.conf` file.


The file above is dynamically generated and concatenates info from:
- `/etc/resolvconf/resolv.conf.d/head` file - so new info can be added manually here, to apper in `/etc/resolv.con` eventually;
- `DHCP` - dynamically provided info (ip, subnet mask, default gw, dns server)

The following should be ran, to apply changes from manually updated above
```
sudo resolvconf -u
```



### DNS: Cache

As it takes a time to get the result, `Local DNS Server` tries to keep in the cache it for some time.

It keeps everything he got from the iterative DNS quering. So for example `www.example.com`, used above, it will remember:
- NS for `.com` (`NS` record);
- NS for `.example.com` (`NS` record);
- IP for `www.example.com` (`A` record).

Thus, if next time `www.primer.com` will be requested by `User Machine`, `Local DNS server` can start asking not from `Root Servers`, but from lower TLD NS for `.com`.

> **NOTE**: The items within a `DNS Cache` are stored for some amount of time, which is defined by the NS, which provides the reply.




### DNS: Headers

`DNS` uses `UDP` for querying.

??? It uses `TCP` to share info between zones. ???


### DNS: Reverse lookup

`DNS` -> `IP`: forward DNS lookup. `IP` -> `DNS`: reverse DNS lookup.

The `NS` resolves info for both directions. So necessary `NS` has to be found out for reverse lookup.

But for forward lookup we have a name structure, that helps us to find necessary `NS` (root -> TLD -> other levels).

For the reverse lookup we have to use a structure as well. After necessary IP is reversed and added with `.in-addr.arpa` at the end, its searching looks pretty similar to the forward DNS lookup: starts with root `NS`, looks for `.in-addr.arpa` `NS`, then looks for the `NS` for 1st octet of IP (in the reversed name its the last one), then octed by octed.

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



# VPN

VPN - Virtual Private Network.

The communication within a private network is usually much trustworthy, then communication between inside and outside of private network.

The goal of VPN is to let computer outside private network to communicate with resources within a private network, as it was inside of private network as well.

The following should be achived to let it happen:
- traffic protected:
  - encrtyption
  - integritiy protection
- authentication implemented 
  - how do we know, that specific computer outside is allowed to be inside of the private network;



## Analogy

There're:
- city `A`;
- city `B`;
- the `bus` (a packet, in terms of communication);
- the `train` (another packet, in terms of communication);
- the `train` is safe way to get from `A` to `B`;
- point `X`;
- point `Y`;
- a dangerous zone, that devides area on 2 halves:
  - 1 half: city `A` and point `X`;
  - 2 half: city `B` and point `Y`;
- direct path between `X` and `Y` is going through dangerous zone, so it's dangeours;
- direct path between city `A` and city `B`is going through dangerous zone as well, but its done with armored `train` with help of railways, so it's safe.


You're on the `bus`.

You need to get from `X` to `Y`. But `X` -> `Y` path is dangerous. 

So you have to use `X` -> `A` -> `B` -> `Y` path, with help of `train`.

And the're 2 ways to do that.


### Analogy: Approach #1: SSH Tunneling (Port Forwarding)

Necessary safe path `X` -> `A` -> `B` -> `Y` is done by:
- buying ticket #1: getting **on** the `bus`;
- getting `X` -> `A` on the `bus` itself;
- going **off** the `bus`;
- buying ticket #2: getting `A` -> `B` on the `train` itself;
- going **off** the `train`;
- buying ticket #3: getting `B` -> `Y` on another `bus` itself;

So you need 3 different tickets to get from `X` to `Y` and get off the ride after each leg of the path:
- bus #1;
- train;
- bus #2.

### Analogy: Approach #2: IP Tunneling

Necessary safe path `X` -> `A` -> `B` -> `Y` is done by:
- buying ticket #1: getting **on** the `bus`;
- getting `X` -> `A` on the `bus` itself;
- the `bus` then goes **on** the `train`;
- getting `A` -> `B` on the `train` (so you're inside of the `bus`, the `bus` is inside of the `train`);
- the `bus` then goes **off** the `train`;
- getting `B` -> `Y` on the `bus` itself;

So you need 1 ticket to the initial `bus` to get from `X` to `Y`, as you never leave the `bus` till the end of the traveling.

In this case instead of buying other tickets, we just ask `bus` driver to do not go `X` -> `Y` directly, but to change route to `X` -> `A` -> `B` -> `Y` instead. But no changes for **your** behaviour you were supposed to go `X` -> `Y`, and you did that (yes, via another path though).



## SSH Tunneling (Port Forwarding)

According to `Analogy: Approach #1` block.

> **NOTE**: It's not the most convenient way. It's here just for education.

Safe path between `A` and `B` is estabslished `SSH` connection between server `A` and server `B`: so data within this connection is encrypted, with integrity kept.

There's a port `8000` (for example) on the server `A`. Everything it gets to this port, is forwarded to the `SSH connection`, to get to the server `B`.

If there's a need to make a direct connection from server `X` to server `Y` via telnet, it's not safe.

But you can get connection from `X` to `A:8000`, then it will be safely forwarded via `SSH` tunnel to `B`, then to the `Y:23`.

In this approach, those a different packets:
- `X` -> `A` is one `TCP` packet;
- `A` -> `B` is another `TCP` packet;
- `B` -> `Y` is another `TCP` packet;

### Example

Make `X` -> `Y` telnet, via safe `A` -> `B` `SSH` tunnel
```
###############
# On server `A`
###############
# Establish SSH tunnel
ssh -L <PORT_A>:<IP_Y>:<PORT_Y> <IP_B>

###############
# On server `X`
###############
# Make a telnet connection
telnet <IP_A> <PORT_A>
```


## IP Tunneling

According to `Analogy: Approach #2` block. 

So it's "put your packet inside other packet" approach.

There're a couple of questions to answer, to make it work.

**Question #1:** How do we get the bus to the train station?

Initially path for bus is `X` -> `Y`, and we want to make it `X` -> `A` for starting.

So routing table are involved.


**Question #2:** How do we get initial packet to another packet?

Once packet gets to the router/computer, it:
- stripped off `MAC Header` (Layer 2), to see what is destination IP within in `IP Header` (Layer 3);
- if current router/computer is not a destination, the packet never leaves `OS kernel`:
  - it has to be send further according to routing rules;
  - a new `MAC Header` (Layer 2) is added to the packet;
  - the packet is sent to further route;
- if current router/computer is a destination, the packet leaves `OS kernel`:
  - headers are stripped off, to get data from the packet from Layer 3 to Layer 7.

Thus, we can see actual data (on application layer, outside of `OS kernel`) only if computer is a destination one. In other case, we never get it higher then `Layer 3`.

So how can we put a packet to another packet, if we don't see it?
- IPSec Approach;
- SSL/TLS Approach (TUN/TAP).

### IP Tunneling: IPSec Approach

As IP packet is always inside a `OS kernel` during routing, `IPSec` was introduced. Which is a sub-protocol of `IP` protocol.

To create a tunnel (a railway between `A` and `B`), you need to create a `IPSec` packet (a `train`), where original `IP` packet (a `bus`) will be put in.

So:
- original IP packet has information within its `IP Header`: IP destination is `X` -> `Y`;
- once original IP packet gets to the `A` server (this is a `train`):
  - a new specific header is added, `IPSec Header`; 
  - original IP packet is considered as a payload to that `IPSec Header`;
  - this payload is encrypted;
  - new `IP Header` is added to the updated packet, which contains another info: IP destination is `A` -> `B`;

You do all of this inside of `OS kernel`. Thus, whenever you have to do any changes to this process, you have to update the `OS kernel`. And modifying `OS kernel` might be no reliable (encryption, key exchange).

So there's another approach.


### IP Tunneling: SSL/TLS Approach (TUN/TAP)

Since 2000, a new technology called `TUN/TAP` was created, to enable the tunneling.

> **NOTE**: The main idea is to provide a way for the `App` to the the **packet itself**, instead of its data.

Usually original IP packet is inside `OS kernel`. If it's correct destination, it's provided to to the higher layers, the headers are stripped off. So `App` eventually gets the data from the packet, but not the packet itself.

> **NOTE**: A `TUN/TAP` is a **virtual interface**, which allows `App` to get entire `IP packet` itself out, to the `Application Layer`. Once it there, `App` can treat is as usual data. Thus, to put it to the new `IP packet` and send it over the network.

So:
- original IP packet has information within its `IP Header`: IP destination is `X` -> `Y`;
- once original IP packet gets to the `A` server:
  - `App` gets the entire packet out of the `OS kernel`, to application layer;
  - sends it to the `B` server, as it would done this with any other usual data (this is the `train`):
    - new `TCP/UDP Header` is added;
    - original `IP packet` is treated as a payload for this new header;
    - this payload is encrypted;
    - new `IP Header` is added: IP destination is `A` -> `B`;

The communication `A` -> `B` between `App` is a normal communication. The only difference is that instead of regular data inside the packet there's another packet.

The advantage of this VPN approach, comparing to previously described `IPSec`: all is done by `App`, so no `OS kernel` modifications has to be done.
If you need to update `App`, you update the `App`. No need to update `OS kernel`.

> **NOTE**: In these days, most of the VPN software uses this `SSL/TLS` (`TUN/TAP`) approach.



## Virtual Networking Technologies: Overall

Unlike the `physical network interface`, which is a piece of hardware, `virtual network interface` is implemented as a piece of software.

Their functionality is similar to `physical network interface`, but they can do many-many more, because they're implemented in software.

The `physical network interface`:
- its one end (#1) is in `OS kernel`, connected with `Network Stack` (the one, that works with packets on MAC, IP and Transport Layers within a kernel);
- its other end (#2) is outside of kernel, physically connected to the wire (in case of Ethernet, for example);
- once `Network Stack` constructs a packet to be sent, its provided to end #1, then a coresponding signal is generated on the end #2 and spread via wire (in case of Ethernet, for example);

The `loopback` is an example of `virtual network interface`:
- we can consider it as 2 pipes:
  - outcoming pipe: for the packets moving from `Network Stack` outside `OS kernel`;
  - incoming pipe: for the opposite direction;
- one end of both (outcoming/incoming) pipes is in `OS kernel`, connected with `Network Stack` (the one, that works with packets on MAC, IP and Transport Layers within a kernel);
- other side of both (outcoming/incoming) pipes is connected with other side of incoming pipe: 
  - whatever goes via outcoming pipe, is automatically redirected to go back to incoming pipe;
  - this virtual interface has IP `127.0.0.1`;
  - that's how everything sent to the IP, comes back;

In the similar way there can be implemented some kind of `black hole` `virtual network interface`:
- whatever packet goes via outcoming pipe, is dropped on its other side;

Or there can be implemented `virtual network interface` that modifies packets:
- whatever packet goes via outcoming pipe, is modified on its other side;
- it can be sent back via incoming pipe then, or sent further over the network;

So many implementations of `virtual network interface` could be done, as this is just a software.


## Virtual Networking Technologies: TUN/TAP

`TUN/TAP` is a type of `virtual network interface`.

It allows `OS kernel` to give the packet to the `App`:
- one end of both (outcoming/incoming) pipes is in `OS kernel`, connected with `Network Stack` (the one, that works with packets on MAC, IP and Transport Layers within a kernel);
- the other end of both (outcoming/incoming) pipes is placed outside of `OS kernel`; but not to the network, but to the `App` instead;
- whatever packet is sent via outcoming pipe, it is got by `App`;
- whatever is sent via incoming pipe (by `App`), is got to `Network Stack` as a packet



Reminder: `Network Stack` within a `OS kernel` consist of:
- Transport layer
- IP layer
- MAC layer

`TUN` interface is connected to `IP layer`.
`TAP` interface is connected to `MAC layer`.

The `OS kernel` has a routing tables, which describe which packet should be sent to which interface.

So:
- if a packet (`IP Header`) has to be sent to `App`, then `TUN` interface will be used;
- if a frame (`MAC Header`) has to be sent to `App`, then `TAP` interface will be used;


> **NOTE**: To build VPN, you can use either of `TUN` or `TAP` interface. 
> But `TAP` interface is used for other applications as well.

> **NOTE**: To be able to use `TUN/TAP` interface, it should have eventually:
> - a new interface itself;
> - IP adress, mapped to the new interface;
> - "UP" state of the new interface.
> For example, `ifconfig` command should show all of that info.

As `TAP` interface can get frames from `Layer 2` to the `App`, it can be sent as usual data over the network to any other location, unpacked and then distributed within new private network via `MAC Adress` as it would be done in the original `private network`.

In this case, information between both `private networks` are distributed in the similar way as it would be one `private network`, physically connected to the one land. This enables data centers to create such `virtual networks` with help of `TAP` interfaces, for example.


## How VPN actually works: Going _To_ Private Network (Client Side)

> **NOTE**: In this part: 
> - how to get to the `train` station on the `bus`;
> - how to load whole `bus` to the armoured `train` at `A`;
> - how the armoured `train` with `bus` inside gets to the `B`.

We have:
- server `A` with VPN client installed:
  - additional `TUN` interface is created;
  - IP address assigned to the `TUN` interface;
- server `B` with VPN server installed;
- server `Y` that need to be reached via VPN eventually;
- servers `A` and `B` are on the different private networks (connected unsafely via Internet);
- servers `B` and `Y` are both on the same private network;

Let's say, we want to ping server `Y` from server `A`, via VPN.

Once command `ping <IP_Y>` started on `A`:
- regular data provided from `App` to `OS kernel`;
- the `Network stack` within a `OS kernel` created initial packet (data + ICMP header + IP header)
  - as we talking about `TUN` interface, the packet is taken from this point (so no MAC header added yet);
- packet goes to the routing table of `A` server;
- previously configured, routing table on `A` says that if network of `<IP_Y>` has to be reached, redirect traffic to the `TUN` interface;
- `TUN` interface then used by `App` (`TUN` program, which is VPN client in our case) to get te original IP packet;
- then `App` encrypts the original IP packet;
- then `App` sends encrypted original IP packet as it would do with regular data, so:
  - socket API is opened;
  - the data (which is encrypted original IP packet) is sent via that opened `socket interface` to the `OS kernel`;
  - the `Network stack` within a `OS kernel` creates new packet, via UDP, for example (data + UDP header + IP header + MAC header):
  - **NOTE**: Now IP header has different info: `A` -> `B`
- then new packet gets to the routing table on `A` again;
- previously configured, routing table on `A` says that if network of `<IP_B>` has to be reached, redirect traffic to the real interface, connected to the network;

New packet safely arrives to the `B`, in a regular approach.


## How VPN actually works: Going _To_ Private Network (Server Side)

> **NOTE**: In this part: 
> - how to take off `bus` from the armoured `train` at `B`;
> - how to get `bus` from `B` to `Y`.

Once new packet (`train` with `bus` inside) arrives to the `B`, where VPN server installed:
- it goes through regular steps:
  - via physical network interface to the `OS kernel`;
  - through its `Network stack`, where all header are stripped off;
  - via regular `socket interface` (with some `App` port mapped to it);
- as of now, content of new packet (which is encrypted original IP packet in this case) is provided to the `App` (`TUN` program, which is VPN server is our case);
- `App` (`TUN` program, which is VPN server is our case) decrypts the data and gets original IP packet;
  - as original destination within original IP packet is `Y`, and we're on `B`, it has to be sent further;
  - but we're just an `App`, we can't route traffic; only `OS kernel` can;
  - thus, we have to give this original IP packet to the `OS kernel`;
  - as an `App`, we can't give the original IP packet via regular `socket interface`, as `OS kernel` would treat it as regular payload, and will struct a new packet again;
- thus, a `TUN` interface will be used by `App` to give whole IP packet to the `OS kernel`;
- but once `OS kernel` on `A` gets IP packet, where `Y` is a destination point:
  - if a server in a `host` mode: it will drop the packet, concidering its some mistake;
  - if a server in a `router` mode: it will try to route the packet to the specified direction;
- so, to turn `router` mode for the server, `IP forwarding` should be enabled;
- the `OS kernel` on `A` then routes IP packet to the `Y`;


## How VPN actually works: Going _From_ Private Network

We have multiple network interfaces on the sending server `A`:
- `TUN` interface (virtual one);
- network interface card (physical one).

Which one is used as the `source IP` for a packet, which is sent via VPN?

> **NOTE**: The `OS kernel` rule:
> In case of multiple network interfaces, the one that sends packet out of the computer, is designated as `source IP` for the packet.

> **NOTE**: This `OS kernel` rule is ONLY applied to the packets, created on this computer.
> If this is a router and just transfering a packet from `A` to `B`, no source IP adress is changed for the packet.


Thus, it differs on each step of the process: 
- it's IP for `TUN` interface when initial IP packet is created and send to the `App` on `A` (because it's `bus`);
- it's IP for `physical network interface card` when updated packet is sent from `A` to `B` (because now it's `train`);




# Firewall











































