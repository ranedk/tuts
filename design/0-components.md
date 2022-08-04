# Components of system design

## Protocols

**Fundamentals**

To relay information between 2 computers on internet, you need the following layers:

1. Network layer - The hardware (Ethernet, mac address, switches, wifi standards etc).
2. Internet layer - The way to identify the Network. IPv4 and IPv6
3. Transport layer - The way to format messages so hardware can understand where it starts and ends. And possible ways to check if some messages were drops and if they need to be played back. TCP, UDP etc.
4. Application layer - Protocols which are desgined for particular applications (like media streaming, multiplexing etc.). HTTP1.1, HTTP2, FTP, Websockets, Webrtc etc.

A better and more accepted model is the OSI model.


### HTTP1.1
Supports Pipelining (ability to send requests without waiting for response).
However, the specification also requires servers to send responses in proper order (no pipelining). This lead to **Head of line blocking** where older delayed responses can block ready new responses. Browsers do not support pipelining on HTTP1.1 because intermediate nodes also need to support pipelining, else it will fail. Since order must be maintained, any bad actor in the network can mangle responses.

### HTTP2
Supports  Multiplexing (ability to send/receive different signals on same connection at once) with a unique ID attached to each request/response. The request/response is called a `Stream`. Because of a unique identifier in every frame (unit of data transfer), the client and the server can dismangle requests and responses and multiplexing works.

`HTTP2` also allows server push when indicated by the client. If the client wants to get a `html` page, it can also specify the `js` and `css` scripts needed for the page such that the server can push those with the html page without client generating any requests. Although `HTTP2` works in non-ssl mode too, most browsers do not let you connect to `HTTP2` without ssl. However, you can do this for server-to-server calls.

However, `HTTP2` is over `TCP` which doesn't isn't multiplexed; meaning that in case of packet loss, since TCP isn't aware of multiplexing (different data frames in one connection), it slows down entire connection and hence all requests/responses. So, `QUIC` (on the top of `UDP`) will also have multiplexing, which means that packet loss will lead to slowing down of only that particular request/response and not all the other data frames. `HTTP3` over `QUIC` will solve this **Head of line blocking** problem for `HTTP2`. Since `UDP` doesn't care about dropped packages, `QUIC` adds the data integrity and ecryption on the top of `UDP`, making it faster than TCP+TLS

>Note: **Anatomy of a connection**: Browsers always send a `HTTP CONNECT` call to make a connection to a proxy. This `HTTP CONNECT` call tells the proxy to forward requests to the domain it is supposed to connect to, or forward the `HTTP CONNECT` call to the next proxy. However, lot of proxies are on the server side or used for caching or in enterprise networks, unknown to the browser (aka transparent proxies). These proxies often remove or add some headers before forwarding the request to the destination.

### Websocket
Complete duplex over UDP. The first handshake is over `HTTP` after which based on headers (`Connection: Upgrade`) the connection is upgraded to `websockets`. `ws` and `wss` (secure) are two schemes used for `websockets`. Very often, proxies support `HTTP(s)` but not long lived connections likes `Websockets`. Also, because `transparent proxies` often strip headers, they will definitely break a websocket connection. However, `transparent proxies` often do not look inside HTTPS connections because of the TLS encryption (they may if they are being used for authentication for example), and hence its better to use `wss` instead of `ws`

### WebRTC
Web Realtime commnunication. For live messaging, torrent, audio/video streaming, where lower latency is required and websocket isn't ideal (given it always goes through a server), `webrtc` was created. Its essentially operates on P2P networks. A server is still required for signaling and connecting peers, but after that, the streaming happens directly between the clients. The server is still capable of backups and transfering data. It uses

- `RTCPeerConnection` for encoding, encryption and processing
- `RTCDataChannel` for data exchange
- `MediaStream API` (works strictly over `https`) for Video/Audio streaming

When you setup a connection, a server acts as a signaling server. The peers send session data (who is connecting (IP), which protocol will be used to connect (websockets/http), codec for data exchange, type of session) to the server. The session data is sent based on SDP (session description protocol), which can be completely opaque to the server. Based on the type of session (e.g. video-offer), the server will send the session data to the peer which matches some criteria with session data and may have a type e.g. video-answer.

After this SDP exchange, the peers will ask a `STUN` server for possible routes to connect to itself and create `ICE candidates`.

Since client machines are behind NAT servers, simple connecting with IP is impossible. To manage this ICE framework is used by Webrtc protocol. (Interactive Connectivity Establishment). The peers keep sending ICE candidates (possible routes) and depending on the best efficient route the connection is established.
If the peer cannot connect based on IP or a STUN server, then TURN server are required.

>NOTE: `STUN servers` - They are public server like a `whats my ip` service which when the client connects, is able to tell the IP of the NAT server and the port to reach a particular client.

If a connectivity via `STUN` server is not possible, a `TURN` server is used which acts like a server through which the webrtc data/media is exchanged. At this step, webrtc stops being a peer to peer connection and the `TURN` server(s) are used to establish connection.

Steps to connect are as follows:
A) Signaling:
    1) Send SDP offer
    2) Start sending all ICE candidates
    3) Receive SDP offer
    4) Receive ICE candidates
B) Connect using `MediaStream` or `RTCDataChannel` APIs over `RTC` (RTC is a protocol on the top of UDP)

The next set of technology enhancement over `Webrtc` will be `Webtransport` which has similar concepts over `QUIC`

### HTTP - DASH (Dynamic adaptive streaming)

This is specialised protocol over `HTTP` for media streaming.
It works by breaking the content into a sequence of small segments (instead of the entire media file), which are served over HTTP. Even live media can be buffered and sent in smaller pieces for a streaming like effect.
It also features a client side bit rate adaptation (ABR) algorithm to automatically select segment with highest possible bit rate without causing a stall or re-buffering. The ABR algorithm itself takes into account the network bandwidth and the screen resolution, while minimizing re-buffering.

## Data exchange frameworks

### REST
Set of guidelines over `HTTP1.1` for GET, POST, PUT, DELETE. Generally uses Json or Xml.

### SOAP
Old complex XML based protocol. Complicated and difficult because of legacy enterprises and Java people.

### gRPC
Google's `RPC` format which standardizes on `protobuf` (binary format) over `HTTP2`. You must define `.proto` files which would generate the client and receiver code. Major advantages on parsing speed, correctness and more data structures over Json or Xml. Because of complexity, it cannot be used in browsers, but is used between server-to-server calls for e.g. in microservices.

### GraphQL
Provides a lot of flexibility for the client to request specific information from the server. It doesn't derive its advantages from `HTTP2` or `protobuf` and is used with `json` very often. While its initial goal was to avoid round trips and get the required strucured data in one go, `HTTP2` manages this better by multiplexing multiple calls into one. `graphQL` is hence more used for its nice API and control on requested data.

Data over these protocols can be further compressed with algorithms like `Kryo`

## Text encoding
UTF-8: Super cool hack to represent ASCII (127 characters) to Unicode (1,114,112 characters). Its a variable length encoding such that initial bits encode the length of the character being represented.
UTF-32: Fixed width and very space wasting.

## Text compression
Huffman encoding: Create a frequency tree and then assign bits based on left or right traversal of tree. Basis of most text encoding methods.

## Rate limiting
Rate limiting for a system can be based on various criteria like per number of requests per second (RPS) or RPS per user or  RPS for a specific user or other parameters like CPU or Memory usage. This would require a data structure to hold config and another to hold number of requests at a given time internal (e.g. total requests every second (by epoch), total requests per minute (by epoch minutes).  We update everytime entries whenever is a new request and is accepted (add to the structure) and when its not needed to hold it (remove from structure)

1. Sliding window approach to manage number of requests per minute (the length the sliding window)
2. Timer wheel approach which manages the slot and also timeout scenario for requests which are taking too long to respond.

**Oracle**: Services register with the Oracle (it can also act as a load balancer and a heart beat system). Services can tell the api rate limit they want for themselves to the Oracle (dynamically via an API) and pass every requests request-id and timestamp to the Oracle. The Oracle can use the above mentioned rate limiting algorithms to manage throttling and timeouts of requests.


